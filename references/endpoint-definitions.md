# Endpoint Definitions for Clinical Trials

## Oncology

### OS (Overall Survival)
- **Definition**: Time from randomization to death from any cause
- **Primary/Secondary**: Primary endpoint in most oncology trials
- **Censoring**: Alive at last follow-up, lost to follow-up
- **Statistical Method**: Kaplan-Meier, log-rank test, Cox proportional hazards

### PFS (Progression-Free Survival)
- **Definition**: Time from randomization to disease progression or death from any cause, whichever occurs first
- **Primary/Secondary**: Primary in many solid tumor trials
- **Assessment**: RECIST 1.1 criteria (radiologic), clinical progression
- **Censoring**: No progression at last assessment, new anticancer therapy started

### ORR (Objective Response Rate)
- **Definition**: Proportion of patients with complete response (CR) or partial response (PR)
- **Primary/Secondary**: Secondary in most trials
- **Assessment**: RECIST 1.1 per investigator or independent review

### DOR (Duration of Response)
- **Definition**: Time from first documented response (CR or PR) to disease progression or death
- **Primary/Secondary**: Secondary
- **Population**: Responders only (conditional endpoint)

## Cardiology

### MACE (Major Adverse Cardiovascular Events)
- **Definition**: Composite of cardiovascular death, non-fatal myocardial infarction, and non-fatal stroke
- **Variations**: Some definitions include coronary revascularization, unstable angina, or hospitalization for unstable angina
- **Primary/Secondary**: Primary in cardiovascular outcome trials (CVOTs)

### HHF (Hospitalization for Heart Failure)
- **Definition**: First hospital admission for heart failure requiring ≥24 hours of acute care
- **Primary/Secondary**: Primary or co-primary in heart failure trials
- **Adjudication**: Independent clinical events committee (CEC) adjudication recommended

### CV Death
- **Definition**: Death due to cardiovascular causes (sudden cardiac death, fatal MI, fatal stroke, heart failure death, other CV)
- **Adjudication**: Requires CEC adjudication; often competing risk with non-CV death

## General

### QoL (Quality of Life)
- **Instruments**: EORTC QLQ-C30, FACT-G, SF-36, disease-specific modules
- **Primary/Secondary**: Secondary in most trials; can be primary in palliative settings
- **Analysis**: Mixed models for repeated measures, responder analysis

### Safety Endpoints
- **AEs**: Adverse events (CTCAE v5.0 grading)
- **SAEs**: Serious adverse events (death, life-threatening, hospitalization, disability, congenital anomaly, other important medical events)
- **Discontinuation**: Treatment discontinuation due to AE
