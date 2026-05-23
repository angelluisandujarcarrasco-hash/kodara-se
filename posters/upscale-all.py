import urllib.request
from PIL import Image
import os

OUT_DIR = r"C:\Users\lucie\kodara-se\posters"

posters = [
    ("01-vine-al-mundo-a-brillar.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101839_af435ea8-ac35-4e4a-bb09-3a182451d9a6.png"),
    ("02-tengo-el-alma-de-mi-abuela.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101843_2385feaa-dca4-45b4-a219-529f8c66d299.png"),
    ("03-las-latinas-no-se-rinden.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101845_a81f767a-d38d-4a45-b93b-6cd75b0226e5.png"),
    ("04-no-eras-una-opcion.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102200_016130e0-02ea-4580-a602-faafafc2d07c.png"),
    ("05-suave-pero-feroz.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101851_e698c437-11c8-4fc2-b6f3-457cdad5cd35.png"),
    ("06-she-believed-she-could.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101854_c32ca03b-e8a9-403b-afda-f9d91886c4ee.png"),
    ("07-good-things-are-coming.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101857_705d1b65-6e0a-466d-adf1-4686135d6dd6.png"),
    ("08-rest-is-productive.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101900_3b8a89cf-6170-42b5-a6a2-ec5a07267214.png"),
    ("09-boundaries-are-beautiful.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101902_0330a8da-75f5-4806-a8df-edc96690be26.png"),
    ("10-i-am-exactly-where.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101905_42f2bfbe-37f2-4d75-91ab-9490fec79ff8.png"),
    ("11-magic-is-in-the-air.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_101908_4db02e39-dcc8-4846-8882-89fa07c10f8e.png"),
    ("12-nunca-es-demasiado-tarde.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102522_3e226be0-1e94-4611-9000-798b1e05bc03.png"),
    ("13-confia-en-tu-proceso.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102524_31386d27-d685-4e8e-ba2b-eaae91861aa1.png"),
    ("14-florece-donde-estes-plantada.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102527_89da41f1-0159-4ff7-801a-b0c915ebe74c.png"),
    ("15-tu-unica-competencia.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102530_54b44e03-9841-45b6-ac17-f5c810852c31.png"),
    ("16-its-never-too-late.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102533_9ac53af3-7cff-4d45-a0f2-f6573cccc044.png"),
    ("17-trust-the-process.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102536_51443eed-322e-4e49-ba22-a0bb118d775b.png"),
    ("18-bloom-where-you-are-planted.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102626_a7c05047-95c0-4c17-b6f7-b2eba770cb1c.png"),
    ("19-your-only-competition.png", "https://d8j0ntlcm91z4.cloudfront.net/user_3DYM1J3h5iy8QkCLK3SvRJRjyvr/hf_20260523_102541_9d74e85b-a8ac-442b-8c07-4e40ab142d70.png"),
]

for i, (filename, url) in enumerate(posters, 1):
    out_path = os.path.join(OUT_DIR, filename)
    tmp_path = out_path + ".tmp"
    try:
        urllib.request.urlretrieve(url, tmp_path)
        img = Image.open(tmp_path)
        img_hi = img.resize((4500, 6000), Image.LANCZOS)
        img_hi.save(out_path, "PNG", dpi=(300, 300), optimize=True)
        os.remove(tmp_path)
        size_mb = os.path.getsize(out_path) / (1024 * 1024)
        print(f"[{i}/19] OK {filename} - {size_mb:.1f} MB")
    except Exception as e:
        print(f"[{i}/19] FAIL {filename}: {e}")

print("DONE")
