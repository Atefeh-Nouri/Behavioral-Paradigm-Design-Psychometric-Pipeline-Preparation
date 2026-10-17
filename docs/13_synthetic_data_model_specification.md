# Synthetic Data Generative Model Specification (Day 13)

## 1. Generative Architecture Overview
The synthetic behavioral data generator uses a hierarchical Monte Carlo architecture linking population-level priors to trial-level Ex-Gaussian response latencies and Signal Detection Theory decision thresholds.

## 2. Mathematical Specification
Subject-level trait sampling uses Normal, TruncatedNormal, Gamma, and Bivariate Normal distributions. Trial-level reaction time generation applies condition modulation, temporal dynamics, and Ex-Gaussian convolution.

## 3. Artifact & Technical Anomaly Rules
Anticipations, attentional lapses, dropped rows, duplicated rows, corrupt RT values, and a stress subject are injected.

## 4. Population Parameter Table
Detailed table lists all parameters with population means, standard deviations, condition shifts, and empirical rationale.
