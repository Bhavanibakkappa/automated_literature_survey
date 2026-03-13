import requests
import os


def download_papers(papers, max_download=50):

    folder = "dataset/papers"

    os.makedirs(folder, exist_ok=True)

    count = 0

    for i, paper in enumerate(papers):

        if count >= max_download:
            break

        url = paper.get("pdf_url")

        if not url:
            continue

        try:

            print(f"Downloading paper {count+1}...")

            response = requests.get(url, timeout=10)

            if response.status_code == 200:

                filename = f"{folder}/paper_{count+1}.pdf"

                with open(filename, "wb") as f:
                    f.write(response.content)

                count += 1

        except Exception as e:
            print("Download failed:", e)

    print(f"\nDownloaded {count} papers successfully.")