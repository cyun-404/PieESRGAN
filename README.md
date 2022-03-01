# Pie-ESRGAN-PyTorch

## Overview

This repository is the code of the paper("Improving ESRGAN with an additional image quality loss" [[Paper]]()).
I referred to the site( https://github.com/Lornatang/ESRGAN-PyTorch (ESRGAN)) for this code.

### Table of contents

- [PieESRGAN-PyTorch](#pie-esrgan-pytorch)
    - [Overview](#overview)
        - [Table of contents](#table-of-contents)
        - [Download weights](#download-weights)
        - [Download dataset](#download-dataset)
            - [Download train dataset](#download-train-dataset)
            - [Download val dataset](#download-val-dataset)
        - [Test (e.g Set5)](#test-eg-set5)
        - [Train (e.g DIV2K)](#train-eg-div2k)
        - [Result](#result)
        - [Contributing](#contributing)
        - [Credit](#credit)
            - [ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks](#esrgan-enhanced-super-resolution-generative-adversarial-networks)

### Download weights

- [Google Driver](https://drive.google.com/file/d/1SBxMk3ofuA217MaNhN71buf94aMDvH7a/view?usp=sharing)


### Download dataset

#### Download train dataset

```bash
cd data/
bash download_dataset.sh
```
use DIV2K.

### Test (e.g Set14)

Modify the contents of the file as follows.

1. `config.py` line 38 `mode="train"` change to `model="valid"`;
2. `config.py` line 104 `model_path=f"results/{exp_name}/g-best.pth"` change to `model_path=f"<YOUR-WEIGHTS-PATH>.pth"`;
3. Run `python validate.py`.

### Train (e.g DIV2K)

Modify the contents of the file as follows.

1. `config.py` line 38 `mode="valid"` change to `model="train"`;
2. Run `python train.py`.

If you want to load weights that you've trained before, modify the contents of the file as follows.

1. `config.py` line 38 `mode="valid"` change to `model="train"`;
2. `config.py` line 56 `start_p_epoch=0` change to `start_p_epoch=XXX`;
3. `config.py` line 58 `resume=False` change to `resume=True`;
4. `config.py` line 59 `resume_p_weight=""` change to `resume_p_weight=<YOUR-RESUME-WIGHTS-PATH>`;
5. Run `python train.py`

### Result


our results: []()
In the following table, the result of the project.
![image](https://user-images.githubusercontent.com/73474866/155973907-c7575c53-8506-4a03-b065-5d3d7faf5441.png)

 ESRGAN / pieESRGAN / Ground Truth
![image](https://user-images.githubusercontent.com/73474866/156099302-63eaf7c7-7f0b-4b0c-af44-e835d2311767.png)


### Contributing

If you find a bug, create a GitHub issue, or even better, submit a pull request. Similarly, if you have questions,
simply post them as GitHub issues.please.


#### Improving ESRGAN with an additional image quality loss

Yunsil choi, Hanhoon park <br>

**Keywords** <br>
image super-resolution, ESRGAN, perceptual loss, PieAPP
```bibtex
@misc{wang2018esrgan,
    title={ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks},
    author={Xintao Wang and Ke Yu and Shixiang Wu and Jinjin Gu and Yihao Liu and Chao Dong and Chen Change Loy and Yu Qiao and Xiaoou Tang},
    year={2018},
    eprint={1809.00219},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```
