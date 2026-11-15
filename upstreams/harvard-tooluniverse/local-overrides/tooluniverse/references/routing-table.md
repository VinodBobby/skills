# ToolUniverse routing table

Read this only when the available skill descriptions do not settle the route or the host does not expose a skill inventory. Load the named package through the host's native mechanism; if that is unavailable, read its `SKILL.md`.

# Routing Table

### 1. Data Retrieval

| Keywords | Action |
|----------|--------|
| "get", "retrieve", "**chemical compound**", "PubChem", "ChEMBL", "drug molecule", "SMILES", "InChI" | `tooluniverse-chemical-compound-retrieval` |
| "get", "retrieve", "**expression data**", "gene expression", "omics dataset", "ArrayExpress", "RNA-seq", "microarray" | `tooluniverse-expression-data-retrieval` |
| "get", "retrieve", "**protein structure**", "PDB", "AlphaFold", "crystal structure", "3D model" | `tooluniverse-protein-structure-retrieval` |
| "get", "retrieve", "**sequence**", "DNA sequence", "RNA sequence", "protein sequence", "FASTA" | `tooluniverse-sequence-retrieval` |
| "**find data**", "**search datasets**", "**dataset**", "where can I get data", "cohort study", "data repository", "public data", "download data for analysis", "what data exists for" | `tooluniverse-dataset-discovery` |
| "**data wrangling**", "download bulk data", "parse format", "API access pattern", "direct API", "raw data download", "beyond tools", "bulk download" | `tooluniverse-data-wrangling` |

### 2. Research & Profiling

| Keywords | Action |
|----------|--------|
| **A single database-checkable fact**, especially multiple-choice — "which of the following gene/drug/variant/pathway is…", anything phrased "**according to** <database>" (DisGeNet, OMIM, MSigDB, miRDB, GTRD, MGI, Ensembl, ClinVar, ChEMBL, OpenTargets, UniProt). Look it up rather than answering from memory; niche annotations are what gets hallucinated | `tooluniverse-biomedical-fact-lookup` |
| "research", "profile", "**disease**", "syndrome", "disorder", "comprehensive report on [disease]" | `tooluniverse-disease-research` |
| "research", "profile", "**drug**", "medication", "therapeutic agent", "tell me about [drug]" | `tooluniverse-drug-research` |
| "**literature review**", "papers about", "publications on", "research articles", "recent studies" | `tooluniverse-literature-deep-research` |
| "research", "profile", "**target**", "protein target", "gene target", "target validation" | `tooluniverse-target-research` |
| "**gene liability**", "gene safety score", "knockout safety", "knockdown safety", "on-target toxicity", "safe to inhibit [gene]" | `tooluniverse-gene-liability` |
| "**peptide target**", "**deorphanize**", "deorphanization", "**peptide off-target**", "what does [peptide] bind", "target of a peptide", "orphan peptide", "peptide doesn't bind [target]", "binds in [species] but not", "find the receptor for [peptide]" | `tooluniverse-peptide-target-deorphanization` |

### 3. Clinical Decision Support

| Keywords | Action |
|----------|--------|
| "**drug safety**", "adverse events", "side effects", "pharmacovigilance", "pharmacogenomics", "FAERS", "black box warning" | `tooluniverse-pharmacovigilance` |
| "**adverse event signal**", "safety signal detection", "disproportionality", "PRR", "ROR" | `tooluniverse-adverse-event-detection` |
| "**drug safety profile**", "drug safety assessment", "comprehensive safety" | `tooluniverse-pharmacovigilance` |
| "**chemical safety**", "ADMET", "chemical toxicity", "environmental toxicity", "toxic effects" | `tooluniverse-chemical-safety` |
| "**cancer treatment**", "precision oncology", "tumor mutation", "targeted therapy", "EGFR", "KRAS", "BRAF" | `tooluniverse-precision-oncology` |
| "**cancer driver**", "driver gene", "driver mutation", "IntOGen", "cBioPortal" | `tooluniverse-cancer-genomics-tcga` |
| "**somatic mutation interpretation**", "cancer variant", "oncogenic variant", "tumor variant" | `tooluniverse-cancer-variant-interpretation` |
| "**ACMG classification**", "variant classification", "benign/pathogenic", "ACMG criteria", "PM2", "PS1", "PP3" | `tooluniverse-acmg-variant-classification` |
| "**cancer classification**", "OncoTree", "tumor subtype", "cancer type code", "histological classification" | `tooluniverse-cancer-classification` |
| "**TCGA**", "cancer genomics cohort", "GDC analysis", "TCGA mutations", "pan-cancer" | `tooluniverse-cancer-genomics-tcga` |
| "**immunotherapy response**", "checkpoint inhibitor response", "TMB", "MSI", "PD-L1", "ICI response" | `tooluniverse-immunotherapy-response-prediction` |
| "**rare disease diagnosis**", "differential diagnosis", "phenotype matching", "HPO", "patient with [symptoms]" | `tooluniverse-rare-disease-diagnosis` |
| "**clinical risk score**", "CHA2DS2-VASc", "HAS-BLED", "CURB-65", "qSOFA", "Child-Pugh", "MELD-Na", "Wells score", "ASCVD risk", "eGFR CKD-EPI", "bedside risk calculator" | `tooluniverse-clinical-risk-scoring` |
| "**device adverse events**", "device recall", "MAUDE", "food/supplement adverse event", "CAERS", "veterinary adverse event", "drug shortage" | `tooluniverse-product-safety-surveillance` |
| "**variant interpretation**", "VUS", "pathogenicity", "clinical significance", "is [variant] pathogenic" | `tooluniverse-variant-interpretation` |
| "**clinical guidelines**", "practice guidelines", "treatment guidelines", "dosing recommendations", "standard of care" | `tooluniverse-clinical-guidelines` |
| **Drug choice for a described patient** — "which of the following is most appropriate for", "which drug should this patient receive"; a vignette naming a modifier (**hepatic/renal impairment**, Child-Pugh, "on a strong CYP3A4 inhibitor", pregnancy, a contraindication) alongside candidate drugs. The deciding fact is in each candidate's FDA label, not recall | `tooluniverse-biomedical-fact-lookup` |
| "**patient stratification**", "precision medicine", "biomarker stratification", "treatment selection" | `tooluniverse-precision-medicine-stratification` |

### 4. Discovery & Design

| Keywords | Action |
|----------|--------|
| "**find binders**", "virtual screening", "hit identification", "compounds for [target]", "**IC50**", "**bioactivity**", "**binding affinity**", "**potency**", "**selectivity**", "**SAR**", "**structure-activity**", "**lead optimization**", "**hit-to-lead**" | `tooluniverse-binder-discovery` |
| "**drug repurposing**", "new indication", "existing drugs for [disease]", "repurpose [drug]" | `tooluniverse-drug-repurposing` |
| "**drug target validation**", "target druggability", "validate target", "target assessment" | `tooluniverse-drug-target-validation` |
| "**network pharmacology**", "polypharmacology", "compound-target network", "multi-target" | `tooluniverse-network-pharmacology` |
| **Ongoing protein design validation** — "protein design campaign", "validate binder candidates", "conflicting binder models", "conditional pH binder", "glycan clash validation", "protein competition submission" | `tooluniverse-protein-design-campaign` |
| "**design protein**", "protein binder", "de novo protein", "RFdiffusion", "ProteinMPNN" | `tooluniverse-protein-therapeutic-design` |
| "**antibody engineering**", "antibody design", "humanization", "affinity maturation" | `tooluniverse-antibody-engineering` |
| "**ADMET prediction**", "ADME", "absorption", "distribution", "metabolism", "excretion", "toxicity prediction" | `tooluniverse-admet-prediction` |
| "**small molecule discovery**", "chemical biology", "compound sourcing", "hit finding", "chemical probe" | `tooluniverse-small-molecule-discovery` |
| "**chemical sourcing**", "buy compound", "vendor search", "Enamine", "MolPort", "compound availability" | `tooluniverse-chemical-sourcing` |
| "**GPCR**", "G-protein coupled receptor", "GPCRdb", "receptor ligand", "biased agonist" | `tooluniverse-gpcr-structural-pharmacology` |
| "**dereplicate**", "natural product identification", "NPAtlas", "ChemOnt classification", "ClassyFire", "producing organism" | `tooluniverse-natural-product-dereplication` |

### 5. Genomics & Variant Analysis

| Keywords | Action |
|----------|--------|
| "**GWAS study**", "genome-wide association", "GWAS catalog", "GWAS for [trait]" | `tooluniverse-gwas-study-explorer` |
| "**GWAS trait to gene**", "trait-associated genes", "causal genes", "genes for [trait]" | `tooluniverse-gwas-trait-to-gene` |
| "**fine-mapping**", "credible sets", "causal variants", "statistical refinement" | `tooluniverse-gwas-finemapping` |
| "**SNP interpretation**", "rsID", "rs[number]", "variant annotation" | `tooluniverse-gwas-snp-interpretation` |
| "**polygenic risk**", "PRS", "genetic risk", "risk score for [disease]" | `tooluniverse-polygenic-risk-score` |
| "**structural variant**", "SV", "CNV", "deletion", "duplication", "chromosomal rearrangement" | `tooluniverse-structural-variant-analysis` |
| "**VCF**", "variant calling", "mutation analysis", "variant annotation pipeline", "**VAF**", "variant allele frequency", "coding variant", "synonymous", "missense" | `tooluniverse-variant-analysis` |
| "**variant functional annotation**", "protein variant effect", "variant consequence", "missense effect" | `tooluniverse-variant-functional-annotation` |
| "**regulatory variant**", "non-coding variant", "eQTL variant", "regulatory region variant" | `tooluniverse-regulatory-variant-analysis` |
| "**rare disease genomics**", "Orphanet gene", "rare disease gene", "causative gene", "exome diagnosis" | `tooluniverse-rare-disease-genomics` |
| "**1000 Genomes**", "IGSR", "population frequency", "superpopulation", "AFR/EUR/EAS/SAS/AMR" | `tooluniverse-population-genetics-1000genomes` |
| "**PheWAS**", "phenome-wide association", "cross-ancestry replication", "cross-biobank", "FinnGen", "BioBank Japan", "pleiotropy of a variant" | `tooluniverse-phewas` |
| "**Mendelian randomization**", "MR causal inference", "instrumental variable", "does X cause Y", "genetic causal evidence" | `tooluniverse-mendelian-randomization` |
| "**loss-of-function mechanism**", "LoF mechanism", "why is this variant LoF", "structural stability vs functional disruption" | `tooluniverse-protein-lof-mechanism` |
| "**SAE feature**", "sparse autoencoder variant", "ESMC SAE", "mechanistic variant interpretation" | `tooluniverse-protein-sae-variant-interpretation` |
| "**per-residue annotation**", "binding interface residues", "ligand pocket residues", "buried vs surface residues", "PDB structural annotation" | `tooluniverse-protein-structural-annotation-pdb` |
| "**why are these residues critical**", "residue functional mechanism", "DMS hotspot interpretation", "catalytic vs structural residue" | `tooluniverse-residue-functional-mechanism-interpretation` |
| "**validate variant predictor**", "DMS validation", "deep mutational scanning benchmark", "predictor vs experimental effect" | `tooluniverse-variant-predictor-dms-validation` |

### 6. Systems & Network Analysis

| Keywords | Action |
|----------|--------|
| "**protein interactions**", "PPI", "interactome", "binding partners", "protein complexes" | `tooluniverse-protein-interactions` |
| "**systems biology**", "pathway analysis", "network analysis", "gene set enrichment" | `tooluniverse-systems-biology` |
| "**metabolomics**", "metabolite identification", "metabolic pathway" | `tooluniverse-metabolomics` |
| "**epigenomics**", "gene regulation", "transcription factor", "TF binding", "enhancers", "chromatin", "ChIP-seq" | `tooluniverse-epigenomics` |
| "**gene enrichment**", "pathway enrichment", "GO enrichment", "GSEA", "overrepresentation", "gene list analysis" | `tooluniverse-gene-enrichment` |
| "**multi-omics**", "omics integration", "transcriptomics + proteomics", "integrated analysis" | `tooluniverse-multi-omics-integration` |
| "**multi-omic disease**", "disease characterization", "genomic + transcriptomic + proteomic" | `tooluniverse-multiomic-disease-characterization` |
| "**gene regulatory network**", "GRN", "TF network", "regulatory circuit", "gene regulation network" | `tooluniverse-gene-regulatory-networks` |
| "**epigenomics chromatin**", "histone modification", "chromatin accessibility", "ATAC-seq", "DNase-seq" | `tooluniverse-epigenomics-chromatin` |
| "**pathway disease**", "disease pathway", "pathway genetics", "pathway convergence" | `tooluniverse-pathway-disease-genetics` |
| "**metabolomics pathway**", "metabolic pathway mapping", "pathway-level metabolomics" | `tooluniverse-metabolomics-pathway` |
| "**interpret results**", "biological context", "beyond p-values", "what does this result mean", "integrate analysis with biology", "statistical results + biology", "causal reasoning", "evidence integration" | `tooluniverse-data-integration-analysis` |

### 7. Screening & Functional Genomics

| Keywords | Action |
|----------|--------|
| "**CRISPR screen**", "genetic screen", "screen hits", "essential genes", "**MAGeCK**", "**sgRNA**", "screen replicate", "screen QC", "dropout screen", "CRISPRa", "CRISPRi", "beta score" | `tooluniverse-crispr-screen-analysis` |
| "**drug-drug interaction**", "DDI", "drug combination", "polypharmacy" | `tooluniverse-drug-drug-interaction` |
| "**differential expression**", "DESeq2", "RNA-seq analysis", "DE genes", "fold change", "differentially expressed", "log2FC", "count matrix", "dispersion" | `tooluniverse-rnaseq-deseq2` |
| "**proteomics**", "mass spectrometry", "protein quantification", "TMT", "iTRAQ", "label-free" | `tooluniverse-proteomics-analysis` |
| "**immune repertoire**", "TCR", "BCR", "T-cell receptor", "B-cell receptor", "clonotype" | `tooluniverse-immune-repertoire-analysis` |
| "**spatial transcriptomics**", "Visium", "MERFISH", "seqFISH", "Slide-seq", "spatial gene expression" | `tooluniverse-spatial-transcriptomics` |
| "**spatial omics**", "spatial proteomics", "spatial multi-omics" | `tooluniverse-spatial-omics-analysis` |
| "**microscopy**", "image analysis", "cell counting", "colony morphometry", "fluorescence quantification" | `tooluniverse-image-analysis` |
| "**electron microscopy**", "cryo-EM", "TEM", "SEM", "EMPIAR", "EMDB" | `tooluniverse-electron-microscopy` |
| "**cell line**", "cell line profiling", "DepMap", "CCLE", "cell line sensitivity" | `tooluniverse-cell-line-profiling` |
| "**clinical data integration**", "clinical phenotype", "EHR analysis", "clinical cohort" | `tooluniverse-clinical-data-integration` |
| "**phylogenetics**", "phylogenetic tree", "sequence alignment", "evolutionary analysis", "treeness", "saturation", "parsimony", "PhyKIT", "DVMC", "long branch", "tree length", "MAFFT", "gap percentage" | `tooluniverse-phylogenetics` |
| "**statistical modeling**", "regression analysis", "logistic regression", "survival analysis", "Cox", "ANOVA", "F-statistic", "chi-square", "spline", "odds ratio", "Cohen's d", "p-value", "clinical trial data", "**ordinal**", "**severity**", "**vaccination**", "SDTM", "DM.csv", "AE.csv", "adverse event severity" | `tooluniverse-statistical-modeling` |
| "**meta-analysis**", "pool effect sizes", "pooled estimate", "evidence synthesis", "forest plot", "heterogeneity", "I-squared", "I²", "fixed-effects", "random-effects", "DerSimonian-Laird", "combine studies", "systematic review statistics", "multi-cohort pooling" | `tooluniverse-meta-analysis` |
| "**dose-response**", "concentration-response", "IC50", "EC50", "Hill slope", "potency", "4-parameter logistic", "4PL", "sigmoidal fit", "Emax", "relative potency", "fold-shift", "drug screening curve" | `tooluniverse-dose-response` |
| "**pharmacokinetics**", "PK analysis", "non-compartmental", "NCA", "Cmax", "Tmax", "AUC", "half-life", "clearance", "volume of distribution", "bioavailability", "concentration-time", "plasma concentration" | `tooluniverse-pharmacokinetics` |
| "**enzyme kinetics**", "Michaelis-Menten", "Km", "Vmax", "kcat", "turnover number", "catalytic efficiency", "specificity constant", "Lineweaver-Burk", "enzyme inhibition", "Ki", "competitive inhibitor" | `tooluniverse-enzyme-kinetics` |
| "**primer design**", "PCR primers", "qPCR primer", "melting temperature", "Tm calculation", "annealing temperature", "GC clamp", "primer-dimer", "oligo analysis", "amplicon", "forward and reverse primer" | `tooluniverse-primer-design` |
| "**diagnostic test**", "sensitivity specificity", "ROC curve", "AUC", "PPV", "NPV", "likelihood ratio", "Youden", "optimal cutoff", "post-test probability", "biomarker accuracy", "confusion matrix" | `tooluniverse-diagnostic-test-evaluation` |
| "**drug synergy**", "drug combination", "Bliss independence", "Loewe additivity", "HSA synergy", "ZIP score", "combination index", "Chou-Talalay", "synergistic antagonistic", "combination therapy analysis" | `tooluniverse-drug-synergy` |
| "**molecular cloning**", "Gibson Assembly", "Golden Gate", "Type IIS", "BsaI", "BbsI", "Esp3I", "BsmBI", "SapI", "assembly overlap", "fragment assembly", "construct design", "domestication", **or the reverse direction** — "I combined these plasmids…", "what does the resulting plasmid express", "what does the gRNA target", "virtual digest", "restriction digest of a plasmid" | `tooluniverse-molecular-cloning` |
| "**metabolomics analysis**", "LC-MS analysis", "metabolite quantification", "metabolic flux" | `tooluniverse-metabolomics-analysis` |
| "**functional genomics screen**", "CRISPR library", "shRNA screen", "barcode screen" | `tooluniverse-functional-genomics-screens` |
| "**proteomics data**", "PRIDE", "MassIVE", "ProteomeXchange", "proteomics dataset" | `tooluniverse-proteomics-data-retrieval` |
| "**protein modification**", "PTM analysis", "phosphorylation site", "ubiquitination", "glycosylation" | `tooluniverse-protein-modification-analysis` |
| "**structural proteomics**", "cross-linking mass spec", "XL-MS", "HDX-MS", "structural biology" | `tooluniverse-structural-proteomics` |
| "**protein structure prediction**", "AlphaFold prediction", "structure modeling", "homology modeling" | `tooluniverse-protein-structure-prediction` |
| "**FASTQ QC**", "FastQC", "MultiQC", "adapter trimming", "fastp", "Cutadapt", "read quality", "sequence duplication" | `tooluniverse-fastq-qc` |

### 8. Clinical Trials & Study Design

| Keywords | Action |
|----------|--------|
| "**clinical trial design**", "trial protocol", "study design", "endpoint selection" | `tooluniverse-clinical-trial-design` |
| "**clinical trial matching**", "patient-to-trial", "trial eligibility", "find trials for patient" | `tooluniverse-clinical-trial-matching` |
| "**GWAS drug discovery**", "genetic target validation", "GWAS to drug" | `tooluniverse-gwas-drug-discovery` |
| "**epidemiological analysis**", "epidemiology", "risk factors", "exposure-outcome", "observational study", "confounder adjustment", "disease risk analysis", "analyze health data", "regression on clinical data", "survival analysis on cohort" | `tooluniverse-epidemiological-analysis` |

### 9. Organism & Evolution

| Keywords | Action |
|----------|--------|
| "**model organism**", "mouse phenotype", "fly ortholog", "worm", "zebrafish", "yeast", "cross-species" | `tooluniverse-model-organism-genetics` |
| "**comparative genomics**", "ortholog", "paralog", "conservation", "evolutionary" | `tooluniverse-comparative-genomics` |
| "**population genetics**", "allele frequency", "HWE", "Fst", "genetic drift" | `tooluniverse-population-genetics` |
| "**plant**", "Arabidopsis", "crop", "plant pathway", "photosynthesis" | `tooluniverse-plant-genomics` |
| "**microbiome**", "metagenomics", "gut bacteria", "16S", "MGnify" | `tooluniverse-metagenomics-analysis` |
| "**pathogen**", "infectious disease", "outbreak", "emerging infection" | `tooluniverse-infectious-disease` |
| "**ecology**", "biodiversity", "invasive species", "pollinator", "food web", "conservation", "community ecology", "trophic" | `tooluniverse-ecology-biodiversity` |
| "**microbiome**", "gut microbiota", "dysbiosis", "microbiome composition", "16S rRNA" | `tooluniverse-microbiome-research` |
| "**adverse outcome pathway**", "AOP", "key event", "molecular initiating event", "KER" | `tooluniverse-adverse-outcome-pathway` |
| "**genome assembly**", "assembly N50", "RefSeq assembly QC", "plasmid count", "NCBI Datasets genome" | `tooluniverse-microbial-genome-characterization` |

### 10. Specialized Biology

| Keywords | Action |
|----------|--------|
| "**lipidomics**", "lipid", "sphingolipid", "ceramide", "fatty acid", "LIPID MAPS" | `tooluniverse-lipidomics` |
| "**miRNA**", "lncRNA", "non-coding RNA", "microRNA", "ncRNA" | `tooluniverse-noncoding-rna` |
| "**aging**", "senescence", "longevity", "senolytic", "geroprotector" | `tooluniverse-aging-senescence` |
| "**vaccine**", "epitope prediction", "MHC binding", "immunogenicity", "T-cell epitope" | `tooluniverse-vaccine-design` |
| "**stem cell**", "iPSC", "organoid", "pluripotency", "differentiation" | `tooluniverse-stem-cell-organoid` |
| "**single cell**", "scRNA-seq", "cell clustering", "UMAP", "cell type" | `tooluniverse-single-cell` |
| "**pharmacogenomics**", "PGx", "CPIC", "CYP2D6", "drug-gene", "genotype-guided dosing" | `tooluniverse-pharmacogenomics` |
| "**drug mechanism**", "mechanism of action", "how does [drug] work", "MOA" | `tooluniverse-drug-mechanism-research` |
| "**drug regulatory**", "FDA approval", "generic availability", "Orange Book", "patent" | `tooluniverse-drug-regulatory` |
| "**gene-disease**", "disease genes", "gene association", "genetic basis" | `tooluniverse-gene-disease-association` |
| "**toxicology**", "AOP", "adverse outcome pathway", "toxin", "BPA" | `tooluniverse-toxicology` |
| "**variant to mechanism**", "how does variant cause disease", "trace variant" | `tooluniverse-variant-to-mechanism` |
| "**regulatory genomics**", "enhancer", "promoter", "ENCODE", "cis-regulatory" | `tooluniverse-regulatory-genomics` |
| "**KEGG disease**", "KEGG drug", "KEGG pathway disease" | `tooluniverse-kegg-disease-drug` |
| "**HLA**", "MHC", "antigen presentation", "transplant compatibility" | `tooluniverse-hla-immunogenomics` |
| "**immunology**", "immune response", "cytokine", "antibody-antigen", "autoimmune", "immune signaling" | `tooluniverse-immunology` |
| "**neuroscience**", "neuron", "brain", "synapse", "neural network", "firing rate", "computational neuroscience", "neuroanatomy", "neurodegeneration", "cranial nerve", "action potential", "connectome" | `tooluniverse-neuroscience` |

### 11. Problem-Solving & Computation

| Keywords | Action |
|----------|--------|
| "**organic chemistry**", "reaction mechanism", "predict product", "NMR interpretation", "IUPAC name", "Diels-Alder", "Grignard", "stereochemistry", "retrosynthesis" | `tooluniverse-organic-chemistry` |
| "**inorganic chemistry**", "crystal structure", "unit cell", "coordination", "point group", "symmetry", "noble gas compound", "lanthanide", "covalency", "bonding theory", "thermodynamics", "Nernst" | `tooluniverse-inorganic-physical-chemistry` |
| "**calculate**", "**compute**", "dosing calculation", "drip rate", "half-life decay", "dilution", "R₀", "herd immunity", "partition function", "pharmacokinetics", "stoichiometry" | `tooluniverse-computational-biophysics` |
| "**neural model**", "firing rate", "integrate-and-fire", "synaptic dynamics", "network model", "balanced network" | `tooluniverse-neuroscience` |
| "**environmental calculation**", "contaminant dilution", "bioconcentration", "mass balance", "environmental fate" | `tooluniverse-computational-biophysics` |

### 12. Infrastructure & Setup

| Keywords | Action |
|----------|--------|
| "**setup**", "install", "configure", "API keys", "upgrade", "**how to use**", "**get started**", "**CLI**", "**tu command**", "MCP vs CLI vs SDK", "**what is ToolUniverse**", "**what can this do**", "**what databases**", "**demo**", "**tutorial**", "**quickstart**", "**I'm new**" | `tooluniverse-claude-code-plugin` |
| "**custom tool**", "add my own tool", "local tool", "create tool", "extend ToolUniverse" | `tooluniverse-custom-tool` |
| "**SDK**", "Python SDK", "build AI scientist", "programmatic access", "**import tooluniverse**", "**coding API**", "**tu build**", "**typed wrappers**" | `tooluniverse-sdk` |
| "**install skills**", "missing skills", "skill not found", "add skills" | `tooluniverse-install-skills` |
| "**self-review**", "eval current work", "evaluate this work", "check my work", "is this complete", "definition of done", "evaluation rubric", "success criteria", "grading criteria", "LLM-as-judge" | `tooluniverse-self-review` |

### 13. Sharing & Account Tasks (you do the work; the user only answers and clicks Allow)

| Keywords | Action |
|----------|--------|
| "**share my model/script/function**", "let my lab/colleague use this", "make this a tool", "share my GPU", "**keep my tool running**" | `tooluniverse-share-computer` |
| "**publish my tool**", "put it in Discover", "let anyone use my tool", "unpublish" | `tooluniverse-publish-tool` |
| "**API key missing**", "login/token rejected", "add my OMIM/NCBI/DisGeNET key", "which logins do I need" | `tooluniverse-database-logins` |
| "**TU-SHARE-**" code, "use my colleague's model/computer", "run it on the lab GPU", "shared or community tools" | `tooluniverse-use-shared-computer` |

---
