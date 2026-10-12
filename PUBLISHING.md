# Publishing and maintaining the website

## Publish from the folder docs/

1. Create an empty GitHub repository, for example `philippine-pfm-atlas`. Do not publish under a government domain, and do not suggest that a government body endorses the atlas.
2. Push the content of this folder to the branch `main` (the commands are in the [README](README.md)). The top level of the repository must contain `docs/`, `src/`, `tools/`, `README.md` and `requirements.txt`, without an extra parent folder above them.
3. Check on GitHub that `docs/index.html` and the hidden file `docs/.nojekyll` are there.
4. Open **Settings**, then **Pages**. Under **Build and deployment**, choose **Deploy from a branch**, the branch `main` and the folder `/docs`, and save.
5. Open the address that **Settings**, **Pages** shows. It is normally `https://USERNAME.github.io/REPOSITORY/`.

GitHub's own instructions:

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

Every page, image, script and style sheet of the website is in `docs/`, so publishing from this folder needs no build on GitHub. The website loads nothing from other servers.

## Update cycle

1. Edit the sources in `src/`: the Markdown files and the diagram code in `src/diagrams/`.
2. Draw the image of each diagram whose code changed: `python tools/render_diagrams.py ID`. The images are in `docs/atlas/rendered/`.
3. Build the atlas: `python tools/build_atlas.py`. Check it: `python tools/check_atlas.py`.
4. Build the website: `python tools/build_site.py`. Check it: `python tools/validate_site.py`.
5. Commit `src/`, `docs/atlas/` and the rest of `docs/` together, and push.

`tools/build_site.py` removes every file of `docs/` except `docs/atlas/` before it writes the website again. A file that is added by hand to `docs/` is therefore lost at the next build. Change the website in `tools/build_site.py` and in `tools/site/`.

Four blocks of the big picture stand between the lines `<!-- site:NAME -->` and `<!-- /site:NAME -->`: the five parts, the four lines, the meeting points and the two cases. The home page shows these blocks. If one of these lines is removed, `tools/build_site.py` stops and names the missing block. The drawing on the home page names the main steps of each line. If the table of the four lines in the big picture no longer contains one of these steps, the script also stops, and the drawing must be changed in `tools/build_site.py` (the list `MAP`).

## Identifiers

The [README](README.md) lists the identifiers that do not change after publication: chapter numbers, reference letters, the numbers of the points of Reference G, the numbers of the rows of the register in Reference B, the source codes, and the diagram IDs. A new item receives the next free number. A removed item leaves its number unused. `tools/build_atlas.py` accepts gaps in the numbers of the register, and stops if a number occurs twice.

## Optional: build and publish with GitHub Actions

The file `deployment/OPTIONAL_pages.yml` is a workflow that is not active. It builds the atlas and the website from `src/` on every push to `main`, runs the checks, and publishes `docs/`. To use it, copy it to `.github/workflows/pages.yml` and set **Settings**, **Pages**, **Source** to **GitHub Actions**. Do not use it together with publishing from a branch. The workflow does not draw images: an image must still be drawn with `tools/render_diagrams.py` and committed when the code of a diagram changes.

## Reports from readers

`.github/ISSUE_TEMPLATE/correction.md` is a form for a GitHub issue. A reader who finds an error, or who has a source for an open point of Reference G, states there where it is, what is wrong or missing, and the source. To receive no such reports, delete the folder `.github/`, or disable **Issues** in **Settings**.

## What the website does not claim

- A flow of data in a diagram does not prove an automatic interface between two programs.
- A planned interface of the IFMIS or of BTMS is not a service in use until a source confirms it.
- A UACS code identifies a class of amounts. It does not identify one payment or one contract.
- The path of one contract and its payment does not apply to payroll, transfers, debt service and the other special payments.
- A circular of one year may change a procedure. Check the version of the circular that applies to the fiscal year.

## Before the repository is made public

- Check that every file is meant for the public, and that quotations and excerpts of other documents are attributed. Citing a document does not give permission to copy it in full.
- Choose a license for the text and the diagrams of the atlas, if others may reuse them. The repository contains no license file. Third-party content keeps its own terms.
- Do not add private contracts, bank account details, signatures, passwords or internal documentation of systems that is not public.
