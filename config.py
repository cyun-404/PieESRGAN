# Copyright 2021 Dakewe Biotech Corporation. All Rights Reserved.
# Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

# ==============================================================================
# File description: Realize the parameter configuration function of data set, model, training and verification code.
# ==============================================================================
import os

import torch
import torch.backends.cudnn as cudnn
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR, MultiStepLR
from torch.utils.tensorboard import SummaryWriter

from model import ContentLoss
from model import Discriminator
from model import Generator

# ==============================================================================
#                              Common configure
# ==============================================================================
torch.manual_seed(0)                       # Set random seed.
upscale_factor   = 4                       # How many times the size of the high-resolution image in the data set is than the low-resolution image.
device           = torch.device("cuda:0")  # Use the first GPU for processing by default.
cudnn.benchmark  = True                    # If the dimension or type of the input data of the network does not change much, turn it on, otherwise turn it off.
mode             = "train"                 # Run mode. Specific mode loads specific variables.
exp_name         = "pie"                # Experiment name.

# ==============================================================================
#                              Train configure
# ==============================================================================
if mode == "train":
    # Configure dataset.
    train_dir             = "data/DFO2K/train"          # The address of the training dataset.
    valid_dir             = "data/DFO2K/valid"          # Verify the address of the dataset.
    image_size            = 128                         # High-resolution image size in the training dataset.
    batch_size            = 4                         # Data batch size.

    # Configure model.
    discriminator         = Discriminator().to(device)  # Load the discriminator model.
    generator             = Generator().to(device)      # Load the generator model.

    # Resume training.
    start_p_epoch         = 0                           # The number of initial iterations of the generator training phase. When set to 0, it means incremental training.
    start_epoch           = 246                           # The number of initial iterations of the adversarial training phase. When set to 0, it means incremental training.
    resume                = False                       # Set to `True` to continue training from the previous training progress.
    resume_p_weight       = ""                          # Restore the weight of the generator model during generator training.
    resume_d_weight       = ""                          # Restore the weight of the generator model during the training of the adversarial network.
    resume_g_weight       = ""                          # Restore the weight of the discriminator model during the training of the adversarial network.

    # Train epochs.
    p_epochs              = 0                        # The total number of cycles of the generator training phase.
    epochs                = 500                         # The total number of cycles in the training phase of the adversarial network.

    # Loss function.
    psnr_criterion        = nn.MSELoss().to(device)     # PSNR metrics.
    pixel_criterion       = nn.L1Loss().to(device)      # Pixel loss.
    content_criterion     = ContentLoss().to(device)    # Content loss.
    adversarial_criterion = nn.BCEWithLogitsLoss().to(device)     # Adversarial loss.
    # Perceptual loss function weight.
    pixel_weight          = 0.01
    content_weight        = 1.0
    adversarial_weight    = 0.005

    # Optimizer.
    p_optimizer           = optim.Adam(generator.parameters(),     0.0002, (0.9, 0.999))  # Generator model learning rate during generator training.
    d_optimizer           = optim.Adam(discriminator.parameters(), 0.0001, (0.9, 0.999))  # Discriminator learning rate during adversarial network training.
    g_optimizer           = optim.Adam(generator.parameters(),     0.0001, (0.9, 0.999))  # Generator learning rate during adversarial network training.

    # Scheduler.
    milestones            = [epochs * 0.125, epochs * 0.250, epochs * 0.500, epochs * 0.750]
    p_scheduler           = CosineAnnealingLR(p_optimizer, p_epochs // 4, 1e-7)               # Generator model scheduler during generator training.
    d_scheduler           = MultiStepLR(d_optimizer, list(map(int, milestones)), 0.5)         # Discriminator model scheduler during adversarial training.
    g_scheduler           = MultiStepLR(g_optimizer, list(map(int, milestones)), 0.5)         # Generator model scheduler during adversarial training.

    # Training log.
    writer                = SummaryWriter(os.path.join("samples",  "logs", exp_name))

    # Additional variables.
    exp_dir1              = os.path.join("samples", exp_name)
    exp_dir2              = os.path.join("results", exp_name)

# ==============================================================================
#                              Validate configure
# ==============================================================================
if mode == "valid":
    # Additional variables.
    exp_dir    = os.path.join("results", "test", exp_name)

    # Load model.
    model      = Generator().to(device)
    model_path = f"results/pieonly/g-best.pth"

    # Test data address.
    lr_dir     = f"data/x4bic/cg_1/"
    sr_dir     = f"results/test/pieonly/"
    hr_dir     = f"data/x4bic/cg1GT/"
