# manim-kor
Manim(3Blue1Brown) Korean channel <br /> 

## manimdef.py 파일?
~~제가 manim 작업하기 편하려고 만든 것입니다. 대부분의 .py 파일에서 이것을 import해서 사용합니다~~ <br />
(25.04.19 - `manimdef.py`는 더 이상 사용되지 않습니다

## raenim
manim 기반 utility tool  
[링크](https://github.com/CodingVillainKor/raenim)에서 설치하신 후 아래와 같이 import해서 사용하실 수 있습니다
```python
from raenim import *

# Scene2D, Scene3D, PythonCode, MINT, ...
``` 

## How to start
### 내 프로젝트 시작하기:
```bash
$ uv init_project.py --name my_manim
```

### Manim impl. 기본기:
1. 클래스가 하나의 영상입니다
2. `manim main.py <class_name>` 실행 시 <class_name>.construct()를 실행합니다
3. 생성된 영상은 `media/`에 저장됩니다


## 1. 비교 연산자 버그
### 아래 연산 결과는? (Guess the result of below code)<br />
**[[YouTube link](https://youtu.be/DA_wD8PKtAM)]**
```python
False == False in [False]
```

```bash
$ cd src
$ uv run manim comparison_bug.py
```


## 2. Radix sort
$O(n^2)$ &nbsp;&nbsp; vs &nbsp;&nbsp; $O(n\textrm{log}n)$ &nbsp;&nbsp; vs &nbsp;&nbsp; $O(n)$
**[[YouTube link](https://www.youtube.com/watch?v=RcGEFETzYjY)]** <br />
Check files in **[[sort folder](https://github.com/CodingVillainKor/manim-kor/tree/main/sort)]**
```bash
$ cd src
$ uv run manim bubblesort.py
$ uv run manim mergesort.py
$ uv run manim plottinggraph.py
$ uv run manim radixsort.py
```

## 3. Attention is all you need 1
" Attention is Weighted sum of values "
**[[YouTube link](https://www.youtube.com/watch?v=3W8B7ma7oFo)]** <br />
Check files in **[[attention folder](https://github.com/CodingVillainKor/manim-kor/tree/main/attention)]**
```bash
$ cd src
$ uv run manim innerprd.py
$ uv run manim main.py
$ uv run manim xtoexp.py
```

## 4. Array Doubling
" Dynamic memory allocation of python list "
**[[YouTube link](https://www.youtube.com/watch?v=PU_EBlEi5U8)]** <br />
Check files in **[[arraydoubling folder](https://github.com/CodingVillainKor/manim-kor/tree/main/arraydoubling)]**
```bash
$ cd src
$ uv run manim arraydoubling.py
$ uv run manim equation.py
$ uv run manim subfootage.py
```


## 5. Big number Multiplication
" Karatsuba algorithm "
**[[YouTube link](https://www.youtube.com/watch?v=S5_9lYB4sAE)]** <br />
```bash
$ cd src
$ uv run manim karatsuba.py
```

## 6. Attention is all you need 2
" Positional encoding and Self-attention "
**[[YouTube link](https://www.youtube.com/watch?v=JST1ZumvUQM)]** <br />
Check files in **[[attention2](https://github.com/CodingVillainKor/manim-kor/tree/main/attention2)]**
```bash
$ cd src
$ uv run manim attention.py
$ uv run manim attention_permute.py
$ uv run manim encdec.py
$ uv run manim pos_enc.py
$ uv run manim pos_enc_permute.py
```

## 7. Attention is all you need 3
" Generation/Training of Transformer, and Masked attention "
**[[YouTube link](https://www.youtube.com/watch?v=s5_TOQozQ3w)]** <br />
Check files in **[[attention3](https://github.com/CodingVillainKor/manim-kor/tree/main/attention3)]**
```bash
$ cd src
$ uv run manim main.py
```

## 8. Short circuit evaluation
" Short circuit evaluation "
**[[YouTube link](https://www.youtube.com/watch?v=5dm7GVsZJLw)]** <br />
Check files in **[[shortcircuit](https://github.com/CodingVillainKor/manim-kor/tree/main/shortcircuit)]**
```bash
$ cd src
$ uv run manim main.py
```

## 9. Hash table
" Hash table (Data structure) "
**[[YouTube link](https://www.youtube.com/watch?v=dQvwCg2DnxA)]** <br />
```bash
$ cd src
$ uv run manim hash_datastructure.py
```

## 10. Maze solver using STACK(DFS)
" Maze solver using Stack (Data structure) "
**[[YouTube link](https://www.youtube.com/watch?v=3fzqQOM4gSs)]** <br />
```bash
$ cd src
$ uv run manim maze_solver.py
```

## 11. Drunk Passenger Problem
" Drunk Passenger Problem "
**[[YouTube link](https://www.youtube.com/watch?v=zznpJFhuLTg)]** <br />
```bash
$ cd src
$ uv run manim drunkpassenger.py
```

## 12. 한글 초 / 중 / 종성 분해 알고리즘
" Hangul unicode order is like stop watch "
**[[YouTube link](https://www.youtube.com/watch?v=2QtG7QbXOPY)]** <br />
```bash
$ cd src
$ uv run manim hangul_stopwatch.py
```

## 13. 생성 모델의 생성은 샘플링
" Generative model's generation is sampling "
**[[YouTube link](https://www.youtube.com/watch?v=ENMtsWy52WA)]** <br />
```bash
$ cd src
$ uv run manim sampling.py
```

## 14. 인코더와 디코더
" Encoding is reducing numbers based on assumption "
**[[YouTube link](https://www.youtube.com/watch?v=WLCDkfFXbj0)]** <br />
```bash
$ cd src/encoder
$ uv run manim main.py
```

## 15. 오토인코더
" AutoEncoder automatically finds rules in data "
**[[YouTube link](https://www.youtube.com/watch?v=Byo7yew9-OQ)]** <br />
```bash
$ cd src
$ uv run manim autoencoder.py
```

## 16. VAE
" When Autoencoder takes adversity, it become VAE, generative model "
**[[YouTube link](https://www.youtube.com/watch?v=q-n2HNan9jo)]** <br />
Requirements: https://github.com/CodingVillainKor/SimpleDeepLearning/blob/main/vae.ipynb 에서 학습시킨 모델 체크포인트 ae.ckpt, aez1.ckpt
```bash
$ cd src/vae
$ uv run manim main.py
```

## 17. Diffusion
" Deriving diffusion loss is quite convoluted "
**[[YouTube link](https://www.youtube.com/watch?v=RGlwzCWJubs)]** <br />
```bash
$ cd src
$ uv run manim diffusion1.py
```

## 18. VQVAE1
Vector quantization
**[[YouTube link](https://youtu.be/mypBS6tPPUA)]** <br />
```bash
$ cd src/vqvae1
$ uv run manim main.py
```

## 19. Neural ODE1
Neural ODE1
**[[YouTube link](https://www.youtube.com/watch?v=afQICWJmpu0)]** <br />
```bash
$ cd src
$ uv run manim node1.py
```

## 20. Neural ODE3
Neural ODE3
**[[YouTube link](https://www.youtube.com/watch?v=UZu2ls-HUlk)]** <br />
```bash
$ cd src
$ uv run manim node3.py
```

## 21. Interior Goat Grazing Problem
Explaining interior goat grazing
**[[YouTube link](https://www.youtube.com/watch?v=feeIKrSsksQ)]** <br />
```bash
$ cd src/goatgrazing
$ uv run manim main.py
```

## 22. Neural ODE4
Neural ODE4
**[[YouTube link]](https://youtu.be/0IjAHl_DV98)** <br />
```bash
$ cd src/node4
$ uv run manim main.py
```

## 23. nn.Linear
pytorch - nn.Linear 설명
**[[YouTube link](https://www.youtube.com/watch?v=zj8_UbOAKkk)]** <br />
```bash
$ cd src
$ uv run manim nnLinear.py
```

## 24. Flow matching 1
Flow matching 1 : Vector field?
**[[YouTube link]](https://www.youtube.com/watch?v=1TCy3sXDP_Q)**  <br />
```bash
$ cd src
$ uv run manim flowmatching1.py
```

## 25. Layer normailization
Pytorch의 layernorm 설명이 헷갈림
[[YouTube link]](https://www.youtube.com/watch?v=r7DRvHmHcNU) <br />
```bash
$ cd src
$ uv run manim layernorm.py
```


## 26. Inheriting nn.Conv
nn.Module이 아니라 nn.Conv를 상속하는 이유
[[YouTube link]](https://www.youtube.com/watch?v=CibhSgvTFGE) <br />
```bash
$ cd src/convbld
$ uv run manim convbld.py
```

## 27. git checkout
`git checkout <commit-hash>` 케이스만
[[YouTube link]](https://www.youtube.com/watch?v=kerEZBJyzEM) <br />
```bash
$ cd src/gitcheckout
$ uv run manim main.py
```


## 28. getattrConfig
getattr()로 고수같이 import하는 법
[[YouTube link]](https://www.youtube.com/watch?v=3_oXQaMdZ-w) <br />
```bash
$ cd src/getattrConfig
$ uv run manim main.py
```

## 29. git reset
`git reset`과 `--soft`, `--mixed`, `--hard` 옵션에 대해
[[YouTube link]](https://www.youtube.com/watch?v=37ki4_QOq4Q) <br />
```bash
$ cd src/gitreset
$ uv run manim main.py
```

## 30. 파이썬의 사소한 3가지
1. \ 뒤에 주석
2. 함수 안 import 범위
3. 숫자 판별을 isnumeric / isdecimal / isdigit으로 하면 안 되는 이유
[[YouTube link]](https://youtu.be/ajWG3lgl5jA) <br />
```bash
$ cd src/trivial_three
$ uv run manim main.py
```

## 31. 단일 브랜치 작업 복습
1. git init/add/commit/checkout/reset
[[YouTube link]](https://youtu.be/-uhhTgD2thU) <br />
```bash
$ cd src/gitsinglebranch
$ uv run manim main.py
```

## 32. Broadcasting
2가지 공식을 기억할 것
[[YouTube link]](https://youtu.be/qebDZAYBLuk) <br />
```bash
$ cd src/broadcasting
$ uv run manim main.py
```

## 33. git branch
새 branch 만들기
[[YouTube link]](https://youtu.be/lQ3NP9kuSx0) <br />
```bash
$ cd src/gitbranch
$ uv run manim main.py
```

## 34. What is uv
uv 후기 및 장단점
[[YouTube link]](https://youtu.be/7_MeE7CdsrM) <br />
```bash
$ cd src/uv1
$ uv run manim main.py
```

## 35. How to uv
uv 후기 및 장단점
[[YouTube link]](https://youtu.be/yQ7QWpaKNvI) <br />
```bash
$ cd src/uv2
$ uv run manim main.py
```

## 36. GIL vs Multithread
" GIL이 있으면 Multithread는 필요없는 거 아님? "
[[YouTube link]](https://youtu.be/KduRAimE7Xk) <br />
```bash
$ cd src/multithreadGIL
$ uv run manim main.py
```

## 37. breakpoint2
" breakpoint 기본, 심화 플로우 "
[[YouTube link]](https://youtu.be/o6st-qW2d7k) <br />
```bash
$ cd src/breakpoint2
$ uv run manim main.py
```

## 38. git merge 1
" git merge 희망편: conflict 없음 "
[[YouTube link]](https://youtu.be/cPthpttoWuE) <br />
```bash
$ cd src/gitmerge1
$ uv run manim main.py
```

## 39. pathlib
pathlib use case: 딥러닝 전처리
[[YouTube link]](https://youtu.be/dO7gAn1hLKU) <br />
```bash
$ cd src/pathlib
$ uv run manim main.py
```

## 40. concurrent.futures
ProcessPoolExecutor
[[YouTube link]](https://youtu.be/KduRAimE7Xk) <br />
```bash
$ cd src/concurrentfutures
$ uv run manim main.py
```

## 41. DiT1
Diffusion Transformer
[[YouTube link]](https://youtu.be/bVV7KhGGAoQ) <br />
```bash
$ cd src/dit1
$ uv run manim main.py
```

## 42. DiT2
Diffusion Transformer2 - Time embedding and conditioning
[[YouTube link]](https://youtu.be/uLjOwMw8l04) <br />
```bash
$ cd src/dit2
$ uv run manim main.py
```

## 43. DiT3
Diffusion Transformer3 - adaLN, adaLN-Zero
[[YouTube link]](https://www.youtube.com/watch?v=0eQVbpfgjqo) <br />
```bash
$ cd src/dit3
$ uv run manim main.py
```

## 44. Flipping coin
Mathematical intuition: Flipping coin
[[YouTube link]](https://youtu.be/gYkzbYuRBdo) <br />
```bash
$ cd src/flipcoin
$ uv run manim main.py
```

## 45. git conflict
Resolving git conflict using VS Code
[[YouTube link]](https://youtu.be/zRQyruIoBVw) <br />
```bash
$ cd src/gitconflict
$ uv run manim main.py
```

## 46. hydra1
hydra is convenient deep learning configuration library
[[YouTube link]](https://youtu.be/T8Ze-rxNytU) <br />
```bash
$ cd src/hydra1
$ uv run manim main.py
```

## 47. git stash
git stash is convenient when you are busy
[[YouTube link]](https://youtu.be/mhZkl7PQBg4) <br />
```bash
$ cd src/gitstash
$ uv run manim main.py
```

## 48. pip install -e .
--editable option is cool
[[YouTube link]](https://youtu.be/9ONtVM7KEB4) <br />
```bash
$ cd src/pipeditable
$ uv run manim main.py
```

## 49. DiT4 (Membership contents)
Looking into DiT official code
[[YouTube link]](https://youtu.be/kE_kvOoZAX0) <br />
```bash
$ cd src/dit4
$ uv run manim main.py
```

## 50. KV cache
How KV cache works
[[YouTube link]](https://youtu.be/sq3XGM1qdQY) <br />
```bash
$ cd src/kvcache
$ uv run manim main.py
```

## 51. Prefill
How prefill works with KV cache
[[YouTube link]](https://youtu.be/Vuu27UTFUZ8) <br />
```bash
$ cd src/prefill
$ uv run manim main.py
```

## 52. \*\*keyword arguments
\*\*keyword arguments in deep learning
[[YouTube link]](https://youtu.be/D4DUd9EoM6s) <br />
```bash
$ cd src/kwargs2025
$ uv run manim main.py
```

## 53. Generator for EDA
Generator let you EDA faster
[[YouTube link]](https://youtu.be/5GYw5sPskvA) <br />
```bash
$ cd src/generator_data
$ uv run manim main.py
```

## 54. hydra3
instantiate is cool
[[YouTube link]](https://youtu.be/S5xSpWTeIA0) <br />
```bash
$ cd src/hydra3
$ uv run manim main.py
```

## 54. speculative decoding
Speculative decoding for faster inference
[[YouTube link]](https://youtu.be/v5al_cwvkJQ) <br />
```bash
$ cd src/spec_decoding
$ uv run manim main.py
```

## 55. contextmanager with an example of timer
contextmanager is defining a covering code block.
[[YouTube link]](https://youtu.be/h1tEZVYFS8A) <br />
```bash
$ cd src/contextmanager
$ uv run manim main.py
```

## 56. EMA1
The concept of Expnential Moving Average
[[YouTube link]](https://youtu.be/KQ_xgw6kueo) <br />
```bash
$ cd src/ema1
$ uv run manim main.py
```

## 57. EMA2
Exponential Moving Average in Deep Learning
[[YouTube link]](https://youtu.be/_cCpG_3clK0) <br />
```bash
$ cd src/ema2
$ uv run manim main.py
```

## 58. git worktree
Git worktree for multiple branches
[[YouTube link]](https://youtu.be/nV9NW899zE8) <br />
```bash
$ cd src/gitworktree
$ uv run manim main.py
```

## 59. Shallow Copy
Shallow copy makes a bug
[[YouTube link]](https://youtu.be/FnSUjR57j-Q) <br />
```bash
$ cd src/shallowcopy
$ uv run manim main.py
```

## 60. Radix sort
Radix sort is O(n)
[[YouTube link]](https://youtu.be/7mfJLJb10hg) <br />
```bash
$ cd src/radixsort
$ uv run manim main.py
```

## 61. DiNO1
Why DiNO is important?
[[YouTube link]](https://youtu.be/r3UBbW0JoMI) <br />
```bash
$ cd src/dino1
$ uv run manim main.py
```
