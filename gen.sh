# export CUDA_VISIBLE_DEVICES="0,1,2,3"
export CUDA_VISIBLE_DEVICES=$1
export VLLM_LOGGING_LEVEL="ERROR"
# nohup bash scripts/gen.sh > ./1.log 2>&1 &

task=$2
models=$3


if [ $task == "0-crossword" ]; then
    cd ./data/$task
    python prompt.py
    cd ../..
    for model in $models; do
        for setting in 5_5 10_10 15_15; do
            task_path=./data/$task/$setting
            prompt_name="prompt.json"
            max_tokens=32768

            python generate.py \
                --model $model \
                --task_path $task_path \
                --prompt_name $prompt_name \
                --temperature 0.0 \
                --top_p 1.0 \
                --max_tokens $max_tokens \
                --vllm \
                --drop_zero_shot
            
            python extract_answer.py \
                --outputs_root ./data/$task/$setting/outputs/$prompt_name/$model \
                --task crossword
        done
    done
elif [ $task == "1-acrostic" ]; then
    cd ./data/$task
    python prompt.py
    cd ../..
    for model in $models; do
        for setting in easy hard; do
            task_path=./data/$task/$setting
            prompt_name="prompt.json"
            max_tokens=32768

            python generate.py \
                --model $model \
                --task_path $task_path \
                --prompt_name $prompt_name \
                --temperature 0.0 \
                --top_p 1.0 \
                --max_tokens $max_tokens \
                --vllm \
                --drop_zero_shot

            python extract_answer.py \
                --outputs_root ./data/$task/$setting/outputs/$prompt_name/$model \
                --task acrostic
        done
    done
elif [ $task == "2-logic" ]; then
    cd ./data/$task
    python prompt.py
    cd ../..
    for model in $models; do
        for setting in 4_4 4_5 4_6 4_7; do
            task_path=./data/$task/$setting
            prompt_name="prompt.json"
            max_tokens=32768

            python generate.py \
                --model $model \
                --task_path $task_path \
                --prompt_name $prompt_name \
                --temperature 0.0 \
                --top_p 1.0 \
                --max_tokens $max_tokens \
                --vllm \
                --drop_zero_shot

            python extract_answer.py \
                --outputs_root ./data/$task/$setting/outputs/$prompt_name/$model \
                --task logic
        done
    done
elif [ $task == "3-cryptogram" ]; then
    cd ./data/$task
    python prompt.py
    cd ../..
    for model in $models; do
        for setting in easy hard; do
            task_path=./data/$task/$setting
            prompt_name="prompt.json"
            max_tokens=32768

            python generate.py \
                --model $model \
                --task_path $task_path \
                --prompt_name $prompt_name \
                --temperature 0.0 \
                --top_p 1.0 \
                --max_tokens $max_tokens \
                --vllm \
                --drop_zero_shot

            python extract_answer.py \
                --outputs_root ./data/$task/$setting/outputs/$prompt_name/$model \
                --task cryptogram
        done
    done
elif [ $task == "4-sudoku" ]; then
    cd ./data/$task
    python prompt.py
    cd ../..
    for model in $models; do
        for setting in 4_4_easy 4_4_hard 9_9_easy 9_9_hard; do
            task_path=./data/$task/$setting
            prompt_name="prompt.json"
            max_tokens=32768

            python generate.py \
                --model $model \
                --task_path $task_path \
                --prompt_name $prompt_name \
                --temperature 0.0 \
                --top_p 1.0 \
                --max_tokens $max_tokens \
                --vllm \
                --drop_zero_shot
            
            python extract_answer.py \
                --outputs_root ./data/$task/$setting/outputs/$prompt_name/$model \
                --task sudoku
        done
    done
elif [ $task == "5-drop" ]; then
    cd ./data/$task
    python prompt.py
    cd ../..
    for model in $models; do
        for setting in easy hard; do
            task_path=./data/$task/$setting
            prompt_name="prompt.json"
            max_tokens=32768

            python generate.py \
                --model $model \
                --task_path $task_path \
                --prompt_name $prompt_name \
                --temperature 0.0 \
                --top_p 1.0 \
                --max_tokens $max_tokens \
                --vllm \
                --drop_zero_shot
            
            python extract_answer.py \
                --outputs_root ./data/$task/$setting/outputs/$prompt_name/$model \
                --task drop
        done
    done
fi