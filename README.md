# manim-kor
Manim(3Blue1Brown) Korean channel <br /> 

### manimdef.py 파일?
~~제가 manim 작업하기 편하려고 만든 것입니다. 대부분의 .py 파일에서 이것을 import해서 사용합니다~~ <br />
(25.04.19 - `manimdef.py`는 더 이상 사용되지 않습니다

### raenim
manim 기반 utility tool  
[링크](https://github.com/CodingVillainKor/raenim)에서 설치하신 후 아래와 같이 import해서 사용하실 수 있습니다
```python
from raenim import *

# Scene2D, Scene3D, PythonCode, MINT, ...
``` 

### How to start
TBU


## 1. 비교 연산자 버그
### 아래 연산 결과는? (Guess the result of below code)<br />
**[[YouTube link](https://youtu.be/DA_wD8PKtAM)]**
```python
False == False in [False]
```

```bash
$ cd src
$ manim comparison_bug.py
```


## 2. Radix sort
$O(n^2)$ &nbsp;&nbsp; vs &nbsp;&nbsp; $O(n\textrm{log}n)$ &nbsp;&nbsp; vs &nbsp;&nbsp; $O(n)$
**[[YouTube link](https://www.youtube.com/watch?v=RcGEFETzYjY)]** <br />
Check files in **[[sort folder](https://github.com/CodingVillainKor/manim-kor/tree/main/sort)]**
```bash
$ cd src
$ manim bubblesort.py
$ manim mergesort.py
$ manim plottinggraph.py
$ manim radixsort.py
```

## 3. Attention is all you need 1
" Attention is Weighted sum of values "
**[[YouTube link](https://www.youtube.com/watch?v=3W8B7ma7oFo)]** <br />
Check files in **[[attention folder](https://github.com/CodingVillainKor/manim-kor/tree/main/attention)]**
```bash
$ cd src
$ manim innerprd.py
$ manim main.py
$ manim xtoexp.py
```

## 4. Array Doubling
" Dynamic memory allocation of python list "
**[[YouTube link](https://www.youtube.com/watch?v=PU_EBlEi5U8)]** <br />
Check files in **[[arraydoubling folder](https://github.com/CodingVillainKor/manim-kor/tree/main/arraydoubling)]**
```bash
$ cd src
$ manim arraydoubling.py
$ manim equation.py
$ manim subfootage.py
```


## 5. Big number Multiplication
" Karatsuba algorithm "
**[[YouTube link](https://www.youtube.com/watch?v=S5_9lYB4sAE)]** <br />
```bash
$ cd src
$ manim karatsuba.py
```

## 6. Attention is all you need 2
" Positional encoding and Self-attention "
**[[YouTube link](https://www.youtube.com/watch?v=JST1ZumvUQM)]** <br />
Check files in **[[attention2](https://github.com/CodingVillainKor/manim-kor/tree/main/attention2)]**
```bash
$ cd src
$ manim attention.py
$ manim attention_permute.py
$ manim encdec.py
$ manim pos_enc.py
$ manim pos_enc_permute.py
```

## 7. Attention is all you need 3
" Generation/Training of Transformer, and Masked attention "
**[[YouTube link](https://www.youtube.com/watch?v=s5_TOQozQ3w)]** <br />
Check files in **[[attention3](https://github.com/CodingVillainKor/manim-kor/tree/main/attention3)]**
```bash
$ cd src
$ manim main.py
```

## 8. Short circuit evaluation
" Short circuit evaluation "
**[[YouTube link](https://www.youtube.com/watch?v=5dm7GVsZJLw)]** <br />
Check files in **[[shortcircuit](https://github.com/CodingVillainKor/manim-kor/tree/main/shortcircuit)]**
```bash
$ cd src
$ manim main.py
```

## 9. Hash table
" Hash table (Data structure) "
**[[YouTube link](https://www.youtube.com/watch?v=dQvwCg2DnxA)]** <br />
```bash
$ cd src
$ manim hash_datastructure.py
```

## 10. Maze solver using STACK(DFS)
" Maze solver using Stack (Data structure) "
**[[YouTube link](https://www.youtube.com/watch?v=3fzqQOM4gSs)]** <br />
```bash
$ cd src
$ manim maze_solver.py
```

## 11. Drunk Passenger Problem
" Drunk Passenger Problem "
**[[YouTube link](https://www.youtube.com/watch?v=zznpJFhuLTg)]** <br />
```bash
$ cd src
$ manim drunkpassenger.py
```

## 12. 한글 초 / 중 / 종성 분해 알고리즘
" Hangul unicode order is like stop watch "
**[[YouTube link](https://www.youtube.com/watch?v=2QtG7QbXOPY)]** <br />
```bash
$ cd src
$ manim hangul_stopwatch.py
```

## 13. 생성 모델의 생성은 샘플링
" Generative model's generation is sampling "
**[[YouTube link](https://www.youtube.com/watch?v=ENMtsWy52WA)]** <br />
```bash
$ cd src
$ manim sampling.py
```

## 14. 인코더와 디코더
" Encoding is reducing numbers based on assumption "
**[[YouTube link](https://www.youtube.com/watch?v=WLCDkfFXbj0)]** <br />
```bash
$ cd src/encoder
$ manim main.py
```

## 15. 오토인코더
" AutoEncoder automatically finds rules in data "
**[[YouTube link](https://www.youtube.com/watch?v=Byo7yew9-OQ)]** <br />
```bash
$ cd src
$ manim autoencoder.py
```

## 16. VAE
" When Autoencoder takes adversity, it become VAE, generative model "
**[[YouTube link](https://www.youtube.com/watch?v=q-n2HNan9jo)]** <br />
Requirements: https://github.com/CodingVillainKor/SimpleDeepLearning/blob/main/vae.ipynb 에서 학습시킨 모델 체크포인트 ae.ckpt, aez1.ckpt
```bash
$ cd src/vae
$ manim main.py
```

## 17. Diffusion
" Deriving diffusion loss is quite convoluted "
**[[YouTube link](https://www.youtube.com/watch?v=RGlwzCWJubs)]** <br />
```bash
$ cd src
$ manim diffusion1.py
```

## 18. VQVAE1
Vector quantization
**[[YouTube link](https://youtu.be/mypBS6tPPUA)]** <br />
```bash
$ cd src/vqvae1
$ manim main.py
```

## 19. Neural ODE1
Neural ODE1
**[[YouTube link](https://www.youtube.com/watch?v=afQICWJmpu0)]** <br />
```bash
$ cd src
$ manim node1.py
```

## 20. Neural ODE3
Neural ODE3
**[[YouTube link](https://www.youtube.com/watch?v=UZu2ls-HUlk)]** <br />
```bash
$ cd src
$ manim node3.py
```

## 21. Interior Goat Grazing Problem
Explaining interior goat grazing
**[[YouTube link](https://www.youtube.com/watch?v=feeIKrSsksQ)]** <br />
```bash
$ cd src/goatgrazing
$ manim main.py
```

## 22. Neural ODE4
Neural ODE4
**[[YouTube link]](https://youtu.be/0IjAHl_DV98)** <br />
```bash
$ cd src/node4
$ manim main.py
```

## 23. nn.Linear
pytorch - nn.Linear 설명
**[[YouTube link](https://www.youtube.com/watch?v=zj8_UbOAKkk)]** <br />
```bash
$ cd src
$ manim nnLinear.py
```

## 24. Flow matching 1
Flow matching 1 : Vector field?
**[[YouTube link]](https://www.youtube.com/watch?v=1TCy3sXDP_Q)**  <br />
```bash
$ cd src
$ manim flowmatching1.py
```

## 25. Layer normailization
Pytorch의 layernorm 설명이 헷갈림
[[YouTube link]](https://www.youtube.com/watch?v=r7DRvHmHcNU) <br />
```bash
$ cd src
$ manim layernorm.py
```


## 26. Inheriting nn.Conv
nn.Module이 아니라 nn.Conv를 상속하는 이유
[[YouTube link]](https://www.youtube.com/watch?v=CibhSgvTFGE) <br />
```bash
$ cd src/convbld
$ manim convbld.py
```

## 27. git checkout
`git checkout <commit-hash>` 케이스만
[[YouTube link]](https://www.youtube.com/watch?v=kerEZBJyzEM) <br />
```bash
$ cd src/gitcheckout
$ manim main.py
```
