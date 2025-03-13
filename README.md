# LR<sup>2</sup>Bench: Evaluating Long-chain Reflective Reasoning Capabilities of Large Language Models via Constraint Satisfaction Problems
<p align="center">
    📖 <a href="https://arxiv.org/abs/2502.17848" target="_blank">Paper</a> • 🤗 <a href="https://huggingface.co/spaces/UltraRonin/LR2Bench" target="_blank">Leaderboard</a>
</p>


Currently, we only provide the data samples without corresponding golden answers. If you wish to test the model's performance or obtain more information, please contact us at our email address: [chenjianghao2022@ia.ac.cn](mailto:chenjianghao2022@ia.ac.cn). We will soon provide an automated evaluation system on our [leaderboard website](https://huggingface.co/spaces/UltraRonin/LR2Bench).


## 💡 Generation
You can edit the tasks and models for generation in `launch.sh`. This script including both model generation and answer extraction.
```bash
bash launch.sh
```
Then run the `merge.sh` to get the JSON file like [submission_template.json](https://github.com/Ultramarine-spec/LR2Bench/blob/main/submission_template.json) for submisson on our Leaderboard website and get your model's performance.
```bash
bash merge.sh
```