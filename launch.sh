for task in 0-crossword 1-acrostic 2-logic 3-cryptogram 4-sudoku 5-drop; do
    bash gen.sh "0,1,2,3" $task "qwen-2.5-7b"
done