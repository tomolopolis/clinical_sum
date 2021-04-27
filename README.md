# Experiments for Estimating Redundnacy in Clinical Texts

There are two notebooks:

1) PPL-Experiments: fine-tunes and estimates PPL (Entropy) for MIMIC-III (Full) & Stroke only, also KCH data (No data is stored in the notebook / this repo)

2) Redundnacy Exploration: Applies summarisation metrics over sequentially ordered notes of the same type, to then aggregate and compare average similarities between pairs of notes of different types

To reproduce results of the MIMIC-III experiments:

- Install the dependencies, (stronly recommend using a virtualenv / venv / conda env).

<pre>
$ conda create -n clinc_redun python=3.7
$ conda activate clinc_redun
$ pip install -r requirements.txt
</pre>

- Download / prepare MIMIC-III. Access available [here](https://mimic.physionet.org/gettingstarted/access/)
- Run each notebook
