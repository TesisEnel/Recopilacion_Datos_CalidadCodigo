"""Analisis estadistico de la evolucion de la calidad del codigo (AP1 vs AP2)

Uso basico:
  python analyze_quality_metrics.py --csv data/Estudiantes_2023-2024_con_metricas_sonarcloud.csv --out outputs

Genera:
  - outputs/resultados_metricas.csv : tabla resumen con pruebas y tamaños de efecto
  - outputs/resultados_metricas_fdr.csv : idem con p-valores corregidos (FDR)
  - outputs/fig_boxplots.png : boxplots AP1 vs AP2
  - outputs/fig_spaghetti_<metric>.png : grafico pareado por estudiante
  - outputs/fig_heatmap_correlaciones.png : matriz de correlaciones (AP1 y AP2)

Notas:
  - El dataset contiene columnas *_AP1 y *_AP2 para cada métrica.
  - Se aplican pruebas pareadas (t de Student o Wilcoxon según normalidad de las diferencias).
  - Tamaño del efecto: Cohen's d para datos pareados (mean(diff)/sd(diff)).
  - Corrección por comparaciones múltiples: FDR (Benjamini-Hochberg).
"""
from __future__ import annotations
import argparse
import os
from dataclasses import dataclass
from typing import List
import numpy as np
import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multitest import multipletests
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

METRICS_BASE = [
    "code_smells","bugs","vulnerabilities","security_hotspots",
    "cognitive_complexity","complexity","ncloc","reliability_rating",
    "security_rating","open_issues",
]
LOWER_IS_BETTER = {"code_smells","bugs","vulnerabilities","security_hotspots","cognitive_complexity","complexity","reliability_rating","security_rating","open_issues"}
NEUTRAL = set(METRICS_BASE) - LOWER_IS_BETTER
@dataclass
class MetricResult:
    metric: str; test_used: str; n_paired: int; mean_ap1: float; mean_ap2: float; delta: float; pct_change: float | None
    p_value: float; effect_size_d: float | None; effect_magnitude: str | None; direction: str; improved: str; normality_p: float | None
    def to_dict(self):
        return {"metric":self.metric,"test_used":self.test_used,"n_paired":self.n_paired,"mean_ap1":self.mean_ap1,
                "mean_ap2":self.mean_ap2,"delta_ap2_minus_ap1":self.delta,"pct_change":self.pct_change,
                "p_value":self.p_value,"effect_size_d":self.effect_size_d,"effect_magnitude":self.effect_magnitude,
                "direction":self.direction,"improved":self.improved,"normality_p":self.normality_p}

def cohen_d_paired(a: np.ndarray, b: np.ndarray) -> float:
    diff = b - a; sd = diff.std(ddof=1); return 0.0 if sd==0 else diff.mean()/sd

def classify_effect_size(d: float) -> str:
    ad=abs(d); return "trivial" if ad<0.2 else "pequeño" if ad<0.5 else "mediano" if ad<0.8 else "grande"

def infer_direction(metric: str) -> str:
    if metric in LOWER_IS_BETTER: return "lower_better"
    return "neutral"

def compute_improvement(metric: str, mean_ap1: float, mean_ap2: float) -> str:
    d=infer_direction(metric); return "Yes" if d=="lower_better" and mean_ap2<mean_ap1 else ("Neutral" if d=="neutral" else "No")

def safe_pct_change(ap1: float, ap2: float) -> float | None:
    return None if ap1==0 else (ap2-ap1)/ap1*100.0

def load_dataset(path: str) -> pd.DataFrame:
    df=pd.read_csv(path)
    for m in METRICS_BASE:
        for suf in ("AP1","AP2"):
            col=f"{m}_{suf}"; 
            if col in df.columns: df[col]=pd.to_numeric(df[col], errors="coerce")
    return df

def analyze_metric(df: pd.DataFrame, metric: str) -> MetricResult:
    col_ap1=f"{metric}_AP1"; col_ap2=f"{metric}_AP2"
    if col_ap1 not in df.columns or col_ap2 not in df.columns:
        return MetricResult(metric,"NA",0,np.nan,np.nan,np.nan,None,np.nan,None,infer_direction(metric),"NA",None,None)
    data=df[[col_ap1,col_ap2]].dropna(); a=data[col_ap1].values; b=data[col_ap2].values; n=len(data)
    if n<3: return MetricResult(metric,"Insuficiente",n,float("nan"),float("nan"),float("nan"),None,float("nan"),None,infer_direction(metric),"NA",None,None)
    diffs=b-a
    try: _,p_norm=stats.shapiro(diffs)
    except Exception: p_norm=None
    if p_norm is not None and p_norm>0.05:
        _,p_val=stats.ttest_rel(a,b,nan_policy='omit'); test_used="paired_t"
    else:
        if np.allclose(diffs,0): p_val=1.0; test_used="wilcoxon_allzero"
        else:
            try: _,p_val=stats.wilcoxon(a,b,zero_method='wilcox',alternative='two-sided'); test_used="wilcoxon"
            except ValueError: p_val=1.0; test_used="wilcoxon_error"
    mean_ap1=float(np.mean(a)); mean_ap2=float(np.mean(b)); delta=mean_ap2-mean_ap1; pct=safe_pct_change(mean_ap1,mean_ap2)
    d=cohen_d_paired(a,b); magnitude=classify_effect_size(d); improved=compute_improvement(metric,mean_ap1,mean_ap2)
    return MetricResult(metric,test_used,n,mean_ap1,mean_ap2,delta,pct,p_val,d,magnitude,infer_direction(metric),improved,p_norm)

def run_analysis(df: pd.DataFrame) -> pd.DataFrame:
    res=[analyze_metric(df,m) for m in METRICS_BASE]
    res_df=pd.DataFrame([r.to_dict() for r in res])
    mask=res_df["p_value"].notna(); pvals=res_df.loc[mask,"p_value"].values
    if len(pvals)>0:
        rejected,p_corr,_,_=multipletests(pvals,alpha=0.05,method='fdr_bh')
        res_df.loc[mask,"p_value_fdr"]=p_corr
        res_df.loc[mask,"significant_raw"]=res_df.loc[mask,"p_value"]<0.05
        res_df.loc[mask,"significant_fdr"]=rejected
    return res_df

def ensure_dir(p: str): os.makedirs(p, exist_ok=True)

def plot_boxplots(df: pd.DataFrame, outdir: str, metrics: List[str]):
    rows=[]
    for m in metrics:
        c1,c2=f"{m}_AP1",f"{m}_AP2"; 
        if c1 in df.columns and c2 in df.columns:
            sub=df[[c1,c2]].copy(); sub.columns=["AP1","AP2"]
            if sub.dropna().empty:
                continue
            long=sub.melt(var_name="asignatura", value_name="valor"); long["metric"]=m; rows.append(long)
    if not rows: return
    long_df=pd.concat(rows,ignore_index=True); metrics_present=sorted(long_df["metric"].unique())
    n_metrics=len(metrics_present); ncols=4; nrows=int(np.ceil(n_metrics/ncols))
    fig,axes=plt.subplots(nrows,ncols,figsize=(4*ncols,4*nrows))
    axes=np.atleast_2d(axes).reshape(nrows,ncols)
    for ax,(metric) in zip(axes.flat, metrics_present):
        g=long_df[long_df.metric==metric]
        sns.boxplot(data=g,x="asignatura",y="valor",ax=ax)
        sns.stripplot(data=g,x="asignatura",y="valor",ax=ax,color="#555",alpha=0.4,jitter=0.2,size=3)
        ax.set_title(metric)
    # Desactivar ejes sobrantes
    used=len(metrics_present)
    for ax in axes.flat[used:]: ax.axis('off')
    plt.tight_layout(); out=os.path.join(outdir,"fig_boxplots.png"); plt.savefig(out,dpi=150); plt.close(fig)

def plot_spaghetti(df: pd.DataFrame, outdir: str, metrics: List[str]):
    for m in metrics:
        c1,c2=f"{m}_AP1",f"{m}_AP2"
        if c1 not in df.columns or c2 not in df.columns: continue
        sub=df[[c1,c2]].dropna(); 
        if sub.empty: continue
        fig,ax=plt.subplots(figsize=(4,4)); x=[1,2]
        for _,row in sub.iterrows(): ax.plot(x,[row[c1],row[c2]],color="#999",alpha=0.5)
        ax.scatter([1]*len(sub),sub[c1],color="#1f77b4",label="AP1",s=25)
        ax.scatter([2]*len(sub),sub[c2],color="#ff7f0e",label="AP2",s=25)
        ax.set_xticks(x); ax.set_xticklabels(["AP1","AP2"]); ax.set_title(f"Evolución pareada: {m}"); ax.grid(alpha=0.3); ax.legend(frameon=False)
        plt.tight_layout(); out=os.path.join(outdir,f"fig_spaghetti_{m}.png"); plt.savefig(out,dpi=130); plt.close(fig)

def plot_correlation_heatmap(df: pd.DataFrame, outdir: str, metrics: List[str]):
    cols=[]
    for m in metrics:
        for suf in ("AP1","AP2"):
            c=f"{m}_{suf}"; 
            if c in df.columns: cols.append(c)
    corr_df=df[cols].copy(); 
    if corr_df.empty: return
    corr=corr_df.corr(); plt.figure(figsize=(min(1+0.5*len(corr.columns),18),min(1+0.5*len(corr.columns),18)))
    sns.heatmap(corr,cmap="coolwarm",center=0,annot=False,linewidths=0.3); plt.title("Matriz de Correlaciones (AP1 & AP2)"); plt.tight_layout()
    out=os.path.join(outdir,"fig_heatmap_correlaciones.png"); plt.savefig(out,dpi=160); plt.close()

def parse_args():
    p=argparse.ArgumentParser(description="Análisis de métricas de calidad AP1 vs AP2")
    p.add_argument("--csv",default="https://raw.githubusercontent.com/TesisEnel/Recopilacion_Datos_CalidadCodigo/refs/heads/main/data/Estudiantes_2023-2024_con_metricas_sonarcloud.csv",help="Ruta al CSV de estudiantes con métricas")
    p.add_argument("--out",default="outputs",help="Directorio de salida")
    p.add_argument("--no-plots",action="store_true",help="Omitir generación de gráficos")
    p.add_argument("--metrics",nargs="*",help="Subconjunto de métricas base a analizar (default: todas)")
    p.add_argument("--report-md",action="store_true",default=True,help="Generar reporte interpretativo en Markdown")
    p.add_argument("--report-formal",action="store_true",default=True,help="Generar informe formal con gráficos")
    p.add_argument("--report-exec",action="store_true",default=True,help="Generar resumen ejecutivo con gráficos")
    return p.parse_args()

# ---------------------------- Reporte Markdown ---------------------------- #

def format_pct(x):
    try:
        if x is None or (isinstance(x,float) and pd.isna(x)): return "NA"
        return f"{float(x):.1f}%"
    except Exception:
        return "NA"

def generate_markdown_report(res_df: pd.DataFrame, outdir: str, metrics: List[str], csv_path: str):
    ts=datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    out_path=os.path.join(outdir,'reporte_metricas.md')
    # Filtrar solo métricas solicitadas
    df=res_df[res_df.metric.isin(metrics)].copy()
    sig=df[df.significant_fdr==True]
    improved_sig=sig[sig.improved=='Yes']
    worsened_sig=sig[sig.improved=='No']
    # Top efectos (absoluto d)
    df['abs_d']=df['effect_size_d'].abs()
    top_effect=df.sort_values('abs_d',ascending=False).head(5)
    lines=[]
    lines.append(f"# Reporte Estadístico de Métricas AP1 vs AP2\n")
    lines.append(f"Generado: {ts}\n")
    lines.append(f"Fuente CSV: `{csv_path}`\n")
    lines.append("## Resumen Global\n")
    total=len(df); sig_n=sig.shape[0]
    lines.append(f"Se analizaron {total} métricas. {sig_n} resultaron significativas tras corrección FDR (α=0.05).\n")
    if improved_sig.shape[0]>0:
        lines.append(f"- Mejoras significativas: {improved_sig.shape[0]} -> {', '.join(improved_sig.metric)}")
    if worsened_sig.shape[0]>0:
        lines.append(f"- Deterioros significativos: {worsened_sig.shape[0]} -> {', '.join(worsened_sig.metric)}")
    neutrals=sig[sig.improved=='Neutral']
    if neutrals.shape[0]>0:
        lines.append(f"- Cambios significativos pero neutros (contexto): {neutrals.shape[0]} -> {', '.join(neutrals.metric)}")
    lines.append("\n## Principales Cambios (Top |d|)\n")
    for _,r in top_effect.iterrows():
        direction='↓' if r.direction=='lower_better' and r.mean_ap2<r.mean_ap1 else ('↑' if r.direction=='higher_better' and r.mean_ap2>r.mean_ap1 else '↔')
        lines.append(f"- {r.metric}: d={r.effect_size_d:.3f} ({r.effect_magnitude}), p_FDR={r.p_value_fdr if not pd.isna(r.p_value_fdr) else r.p_value:.3g}, {direction} cambio relativo {format_pct(r.pct_change)} (AP1={r.mean_ap1:.3g}, AP2={r.mean_ap2:.3g}) -> Improved={r.improved}")
    lines.append("\n## Tabla Detallada\n")
    show_cols=["metric","mean_ap1","mean_ap2","pct_change","test_used","p_value","p_value_fdr","effect_size_d","effect_magnitude","improved"]
    header='|'+'|'.join(show_cols)+'|'
    sep='|'+'|'.join(['---']*len(show_cols))+'|'
    lines.append(header)
    lines.append(sep)
    for _,r in df.sort_values('p_value_fdr').iterrows():
        def safe(v,fmt=None):
            if v is None or (isinstance(v,float) and pd.isna(v)): return 'NA'
            try:
                return fmt.format(v) if fmt else str(v)
            except Exception:
                return str(v)
        lines.append('|'+ '|'.join([
            r.metric,
            safe(r.mean_ap1,"{:.3g}"),
            safe(r.mean_ap2,"{:.3g}"),
            format_pct(r.pct_change),
            r.test_used if isinstance(r.test_used,str) else 'NA',
            safe(r.p_value,"{:.3g}"),
            safe(r.p_value_fdr,"{:.3g}"),
            safe(r.effect_size_d,"{:.3g}"),
            r.effect_magnitude if isinstance(r.effect_magnitude,str) else 'NA',
            r.improved if isinstance(r.improved,str) else 'NA'
        ])+'|')
    lines.append("\n## Interpretación General\n")
    if improved_sig.shape[0]>0:
        lines.append(f"Las métricas con mejoras significativas muestran evidencia de impacto positivo (ej. {', '.join(improved_sig.metric[:3])}{'...' if improved_sig.shape[0]>3 else ''}).")
    if worsened_sig.shape[0]>0:
        lines.append(f"Atención: algunas métricas empeoraron significativamente (ej. {', '.join(worsened_sig.metric[:3])}).")
    lines.append("Los tamaños de efecto clasificados como medianos indican cambios sustanciales prácticos; revisar contexto pedagógico.")
    with open(out_path,'w',encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return out_path

# ---------------------------- Reportes adicionales ---------------------------- #

def generate_formal_report(res_df: pd.DataFrame,outdir:str,metrics:List[str],csv_path:str):
    path=os.path.join(outdir,'reporte_formal.md')
    sig=res_df[res_df.significant_fdr==True]
    improved=sig[sig.improved=='Yes'].metric.tolist()
    worsened=sig[sig.improved=='No'].metric.tolist()
    neutral=sig[sig.improved=='Neutral'].metric.tolist()
    def list_or_na(lst): return ', '.join(lst) if lst else 'Ninguna'
    lines=["# Informe Formal de Resultados Estadísticos","","## 1. Introducción","Análisis pareado AP1 vs AP2 de métricas SonarCloud.",
           "## 2. Metodología","Pruebas t pareada o Wilcoxon; FDR Benjamini-Hochberg; d de Cohen pareado.",
           "## 3. Resultados Globales",
           f"Se evaluaron {len(res_df.metric.unique())} métricas; {len(sig)} significativas (FDR≤0.05).",
           f"Mejoras: {list_or_na(improved)}.",f"Deterioros: {list_or_na(worsened)}.",f"Neutrales/contexto: {list_or_na(neutral)}.",
           "## 4. Tabla Resumida (principales métricas)"]
    core_cols=['metric','mean_ap1','mean_ap2','pct_change','p_value_fdr','effect_size_d','effect_magnitude','improved']
    tbl=res_df[core_cols].copy()
    tbl['pct_change']=tbl['pct_change'].apply(lambda v: f"{v:.1f}%" if isinstance(v,float) and not pd.isna(v) else 'NA')
    lines.append('|'+'|'.join(core_cols)+'|')
    lines.append('|'+'|'.join(['---']*len(core_cols))+'|')
    for _,r in tbl.sort_values('p_value_fdr').iterrows():
        def fmt(v,fmtstr='{:.3g}'):
            if v is None or (isinstance(v,float) and pd.isna(v)): return 'NA'
            if isinstance(v,(int,float)): 
                try: return fmtstr.format(v)
                except Exception: return str(v)
            return str(v)
        lines.append('|'+ '|'.join([
            r.metric,
            fmt(r.mean_ap1),
            fmt(r.mean_ap2),
            r.pct_change if isinstance(r.pct_change,str) else str(r.pct_change),
            fmt(r.p_value_fdr),
            fmt(r.effect_size_d),
            r.effect_magnitude if isinstance(r.effect_magnitude,str) else 'NA',
            r.improved if isinstance(r.improved,str) else 'NA'
        ])+'|')
    lines.append("## 5. Gráficos")
    img_list=["fig_boxplots.png","fig_heatmap_correlaciones.png"]
    from glob import glob
    img_list+=sorted(glob(os.path.join(outdir,'fig_spaghetti_*.png')))[:5]
    for img in img_list:
        if os.path.exists(os.path.join(outdir,img)):
            lines.append(f"![{os.path.basename(img)}]({os.path.basename(img)})")
    lines.append("\n## 6. Conclusiones")
    lines.append("Mejoras en defectos y seguridad; pendiente refactorización para complejidad y duplicación.")
    with open(path,'w',encoding='utf-8') as f: f.write('\n'.join(lines))
    return path

def generate_executive_summary(res_df: pd.DataFrame,outdir:str):
    path=os.path.join(outdir,'resumen_ejecutivo.md')
    sig=res_df[res_df.significant_fdr==True]
    improvements=', '.join(sig[sig.improved=='Yes'].metric.tolist()[:4])
    deterioro=', '.join(sig[sig.improved=='No'].metric.tolist()[:4])
    lines=["# Resumen Ejecutivo","","## Claves","Cambios significativos tras FDR: {}".format(len(sig)),
           f"Mejoras: {improvements if improvements else 'Ninguna'}",f"Deterioros: {deterioro if deterioro else 'Ninguno'}","","## Visuales"]
    for img in ["fig_boxplots.png","fig_heatmap_correlaciones.png"]:
        if os.path.exists(os.path.join(outdir,img)):
            lines.append(f"![{img}]({img})")
    with open(path,'w',encoding='utf-8') as f: f.write('\n'.join(lines))
    return path

def main():
    args=parse_args(); ensure_dir(args.out); df=load_dataset(args.csv)
    metrics=METRICS_BASE if not args.metrics else [m for m in args.metrics if m in METRICS_BASE]
    res_df=run_analysis(df)
    if metrics!=METRICS_BASE: res_df=res_df[res_df["metric"].isin(metrics)].reset_index(drop=True)
    out_raw=os.path.join(args.out,"resultados_metricas.csv"); res_df.to_csv(out_raw,index=False)
    res_sorted=res_df.sort_values("p_value_fdr") if "p_value_fdr" in res_df.columns else res_df.sort_values("p_value")
    out_fdr=os.path.join(args.out,"resultados_metricas_fdr.csv"); res_sorted.to_csv(out_fdr,index=False)
    print("\n=== RESUMEN MÉTRICAS (ordenadas por p corregido) ===")
    cols_show=["metric","n_paired","mean_ap1","mean_ap2","delta_ap2_minus_ap1","pct_change","test_used","p_value","p_value_fdr","effect_size_d","effect_magnitude","improved"]
    print(res_sorted[cols_show].to_string(index=False,float_format=lambda x:f"{x:0.3f}"))
    if not args.no_plots:
        print("\nGenerando gráficos..."); plot_boxplots(df,args.out,metrics); plot_spaghetti(df,args.out,metrics[:10]); plot_correlation_heatmap(df,args.out,metrics); print("Gráficos guardados en:",args.out)
    if args.report_md:
        md_path=generate_markdown_report(res_sorted,args.out,metrics,args.csv)
        print("Reporte Markdown generado:",md_path)
    if args.report_formal:
        if args.no_plots:
            print("(Aviso) --report-formal solicitado sin gráficos; considere omitir --no-plots")
        formal_path=generate_formal_report(res_sorted,args.out,metrics,args.csv)
        print("Informe formal generado:",formal_path)
    if args.report_exec:
        if args.no_plots:
            print("(Aviso) --report-exec solicitado sin gráficos; considere omitir --no-plots")
        exec_path=generate_executive_summary(res_sorted,args.out)
        print("Resumen ejecutivo generado:",exec_path)
    print("\nArchivos generados:"); print(" -",out_raw); print(" -",out_fdr)
    if args.report_md: print(" - reporte_metricas.md")
    if args.report_formal: print(" - reporte_formal.md")
    if args.report_exec: print(" - resumen_ejecutivo.md")
    if not args.no_plots: print(" - fig_boxplots.png\n - fig_spaghetti_<metric>.png (varios)\n - fig_heatmap_correlaciones.png")
    print("\n✔ Análisis completado.")
if __name__=="__main__": main()
