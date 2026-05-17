# Hosting the Model on Zenodo &amp; Minting a DOI

A Zenodo deposit turns the trained model from a private file into a citeable, version-pinned research output, gives the repository a persistent DOI, and produces the badge that appears at the top of the main `README.md`. The process is free, takes about ten minutes, and only needs to be done once per dissertation version.

## 1. Create a Zenodo Account

Zenodo is operated by CERN and accepts logins through ORCID, GitHub, or email. Signing in with the same ORCID iD that you list in `CITATION.cff` is recommended because Zenodo will then automatically attach the deposit to your ORCID record.

## 2. Create a New Upload

From the Zenodo dashboard, choose *New upload* and fill in the metadata.

The **resource type** should be set to *Software*. The **title** should match the project title used in the README and `CITATION.cff`, namely *Spatio-Temporal Crop Health Assessment for the Jammu Region using Multi-Source Remote Sensing and Machine Learning*. Add yourself as an author with your ORCID iD and affiliation, paste in the abstract from `CITATION.cff`, and add the same keyword list. Set the **license** to MIT to match the repository, and set the version to `1.0.0`.

In the **files** section, upload `Best_model.pkl`. Zenodo accepts files up to 50 GB per deposit, so the 228 MB model is well within limits.

In the **related identifiers** section, add the GitHub repository URL with relation type *is supplement to*. This creates a bidirectional link between the GitHub release and the Zenodo deposit.

## 3. Publish and Capture the DOI

When you click *Publish*, Zenodo issues two DOIs: a *concept DOI* that always resolves to the latest version of the deposit, and a *version DOI* that points specifically at the `1.0.0` release. For dissertation purposes, the concept DOI is the one you want in the README badge and in your written thesis, because it remains valid if you later upload an updated model.

Both DOIs are visible on the published record page.

## 4. Wire the DOI into the Repository

Open `README.md` and locate the commented-out badge block near the top:

```html
<!--
Once you mint a DOI on Zenodo (see docs/ZENODO.md), uncomment and edit:
<a href="https://doi.org/10.5281/zenodo.XXXXXXX"><img alt="DOI" src="https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg"></a>
-->
```

Replace both occurrences of `XXXXXXX` with the numeric portion of your concept DOI (everything after `10.5281/zenodo.`), and remove the surrounding `<!--` and `-->` comment markers. The badge will then render in the badge row.

Next, open `CITATION.cff` and uncomment the two lines under the `TODO` comment, substituting your concept DOI:

```yaml
doi: "10.5281/zenodo.XXXXXXX"
url: "https://doi.org/10.5281/zenodo.XXXXXXX"
```

Finally, open `scripts/download_model.py` and replace `MODEL_URL` with the direct file URL from your Zenodo record. It follows the pattern `https://zenodo.org/records/<id>/files/Best_model.pkl`, where `<id>` is the numeric record identifier shown in the URL of the published deposit page.

After these three edits, anyone cloning the repository can fetch the exact model used in your dissertation with one command, GitHub will display a one-click *Cite this repository* button that resolves to the Zenodo DOI, and your repository becomes a properly archived research output rather than a transient code dump.

## 5. Optional — Automatic GitHub ⇄ Zenodo Sync

For future releases, Zenodo offers a GitHub integration that automatically archives every tagged GitHub release as a new Zenodo version. The setup is documented at [https://docs.github.com/repositories/archiving-a-github-repository/referencing-and-citing-content](https://docs.github.com/repositories/archiving-a-github-repository/referencing-and-citing-content). This is a useful long-term habit but is not required for the initial dissertation submission.
