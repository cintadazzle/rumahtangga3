import os
import zipfile
import json

def create_zip():
    print("Membuat zip project...")
    zipf = zipfile.ZipFile('app_for_colab.zip', 'w', zipfile.ZIP_DEFLATED)
    exclude_dirs = {'.git', '.venv', 'venv', '__pycache__', '.buildozer', 'bin', 'build'}
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            if file.endswith('.zip') or file.endswith('.ipynb') or file == 'prepare_colab.py':
                continue
            file_path = os.path.join(root, file)
            zipf.write(file_path, os.path.relpath(file_path, '.'))
    zipf.close()
    print("Berhasil membuat app_for_colab.zip!")

def create_notebook():
    print("Membuat notebook Google Colab...")
    notebook_content = {
      "nbformat": 4,
      "nbformat_minor": 0,
      "metadata": {
        "colab": {
          "name": "Build_APK_Colab.ipynb",
          "provenance": []
        },
        "kernelspec": {
          "name": "python3",
          "display_name": "Python 3"
        }
      },
      "cells": [
        {
          "cell_type": "markdown",
          "metadata": {
            "id": "intro"
          },
          "source": [
            "# Build Kivy App to APK menggunakan Buildozer\n",
            "1. Jalankan cell pertama untuk menginstall semua dependensi yang dibutuhkan.\n",
            "2. Upload file `app_for_colab.zip` ke dalam Colab (melalui panel **Files** berbentuk icon folder di sebelah kiri).\n",
            "3. Jalankan cell kedua untuk mengekstrak project dan memulai proses build APK.\n",
            "4. Setelah selesai (bisa memakan waktu 10-15 menit), download file APK yang ada di dalam folder `bin/`."
          ]
        },
        {
          "cell_type": "code",
          "metadata": {
            "id": "install"
          },
          "source": [
            "!pip install buildozer\n",
            "!pip install cython==0.29.33\n",
            "!sudo apt-get update\n",
            "!sudo apt-get install -y build-essential libltdl-dev libffi-dev libssl-dev python3-dev zip unzip\n",
            "!sudo apt-get install -y git openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libmtdev1"
          ],
          "execution_count": None,
          "outputs": []
        },
        {
          "cell_type": "code",
          "metadata": {
            "id": "build"
          },
          "source": [
            "import os\n",
            "import zipfile\n",
            "\n",
            "if os.path.exists('app_for_colab.zip'):\n",
            "    print('Mengekstrak file zip...')\n",
            "    with zipfile.ZipFile('app_for_colab.zip', 'r') as zip_ref:\n",
            "        zip_ref.extractall('my_app')\n",
            "    \n",
            "    os.chdir('my_app')\n",
            "    print('Memulai proses buildozer...')\n",
            "    !yes | buildozer android debug\n",
            "    print('Selesai! Cek folder my_app/bin/ untuk mengambil APK kamu.')\n",
            "else:\n",
            "    print('Error: app_for_colab.zip tidak ditemukan. Silakan upload file tersebut di panel sebelah kiri terlebih dahulu.')"
          ],
          "execution_count": None,
          "outputs": []
        }
      ]
    }
    
    with open('Build_APK_Colab.ipynb', 'w') as f:
        json.dump(notebook_content, f, indent=2)
    print("Berhasil membuat Build_APK_Colab.ipynb!")

if __name__ == '__main__':
    create_zip()
    create_notebook()
