# ****** BLIP-2 ******
from PIL import Image
import torch
from lavis.models import load_model_and_preprocess
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)

def load_demo_image(device, img_name):
    # img_url = "images/VOA_EN_NW_2015.08.11.2913549_3.jpg"
    raw_image = Image.open(f'{img_name}', "r").convert('RGB')
    return raw_image

# loads BLIP-2 pre-trained model
model, vis_processors, _ = load_model_and_preprocess(name="blip2", model_type="pretrain", is_eval=True, device=device)

import glob
import csv
import pandas as pd
images2, descrip = [], []
output_cap_des = pd.DataFrame()
# output_cap_des = pd.read_csv('output.tsv', sep='\t')
images_list = glob.glob("images/*.jpg")
# with open("output_desc.txt", 'w') as f:
for image_name in images_list:
    print(image_name)
    r_image = load_demo_image(device=device, img_name=image_name)
    # prepare the image
    image = vis_processors["eval"](r_image).unsqueeze(0).to(device)

    # model.generate({"image": image, "prompt": "Question: which city is this? Answer:"})
    # answer = model.generate({"image": image, "prompt": "Question: Write a piece of news that goes along this photo. Answer:"})
    answer = model.generate({"image": image, "prompt": "Question: Describe the event that is taking place in this photo. Answer:"})
    print('description: ' + answer[0])
    images2.append(image_name)
    descrip.append(answer[0])

#         f.writelines(image_name + "," + answer[0] )
# f.close()
output_cap_des["image2"] = images2
output_cap_des["description"] = descrip
output_cap_des.to_csv("output_cap_des.tsv", sep='\t')