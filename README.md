# manim-kor
Manim(3Blue1Brown) Korean channel <br /> 

### manimdef.py 파일?
제가 manim 작업하기 편하려고 만든 것입니다. 대부분의 .py 파일에서 이것을 import해서 사용합니다

## 1. 비교 연산자 버그
### 아래 연산 결과는? (Guess the result of below code)<br />
**[[YouTube link](https://youtu.be/DA_wD8PKtAM)]**
```python
False == False in [False]
```

### manim 영상 렌더링 방법: (How to render manim)<br />
```bash
$ manim comparison_bug.py
```


## 2. Radix sort
$O(n^2)$ &nbsp;&nbsp; vs &nbsp;&nbsp; $O(n\textrm{log}n)$ &nbsp;&nbsp; vs &nbsp;&nbsp; $O(n)$
**[[YouTube link](https://www.youtube.com/watch?v=RcGEFETzYjY)]** <br />
Check files in **[[sort folder](https://github.com/CodingVillainKor/manim-kor/tree/main/sort)]**
```bash
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
$ manim innerprd.py
$ manim main.py
$ manim xtoexp.py
```

## 4. Array Doubling
" Dynamic memory allocation of python list "
**[[YouTube link](https://www.youtube.com/watch?v=PU_EBlEi5U8)]** <br />
Check files in **[[arraydoubling folder](https://github.com/CodingVillainKor/manim-kor/tree/main/arraydoubling)]**
```bash
$ manim arraydoubling.py
$ manim equation.py
$ manim subfootage.py
```


## 5. Big number Multiplication
" Karatsuba algorithm "
**[[YouTube link](https://www.youtube.com/watch?v=S5_9lYB4sAE)]** <br />
```bash
$ manim karatsuba.py
```

## 6. Attention is all you need 2
" Positional encoding and Self-attention "
**[[YouTube link](https://www.youtube.com/watch?v=JST1ZumvUQM)]** <br />
Check files in **[[attention2](https://github.com/CodingVillainKor/manim-kor/tree/main/attention2)]**
```bash
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
$ manim main.py
```

## 8. Short circuit evaluation
" Short circuit evaluation "
**[[YouTube link](https://www.youtube.com/watch?v=5dm7GVsZJLw)]** <br />
Check files in **[[shortcircuit](https://github.com/CodingVillainKor/manim-kor/tree/main/shortcircuit)]**
```bash
$ manim main.py
```

## 9. Hash table
" Hash table (Data structure) "
**[[YouTube link](https://www.youtube.com/watch?v=dQvwCg2DnxA)]** <br />
```bash
$ manim hash_datastructure.py
```

## 10. Maze solver using STACK(DFS)
" Maze solver using Stack (Data structure) "
**[[YouTube link](https://www.youtube.com/watch?v=3fzqQOM4gSs)]** <br />
```bash
$ manim maze_solver.py
```

## 11. Drunk Passenger Problem
" Drunk Passenger Problem "
**[[YouTube link](https://www.youtube.com/watch?v=zznpJFhuLTg)]** <br />
```bash
$ manim drunkpassenger.py
```

## 12. 한글 초 / 중 / 종성 분해 알고리즘
" Hangul unicode order is like stop watch "
**[[YouTube link](https://www.youtube.com/watch?v=2QtG7QbXOPY)]** <br />
```bash
$ manim hangul_stopwatch.py
```

## 13. 생성 모델의 생성은 샘플링
" Generative model's generation is sampling "
**[[YouTube link](https://www.youtube.com/watch?v=ENMtsWy52WA)]** <br />
```bash
$ manim sampling.py
```

## 14. 인코더와 디코더
" Encoding is reducing numbers based on assumption "
**[[YouTube link](https://www.youtube.com/watch?v=WLCDkfFXbj0)]** <br />
```bash
$ cd encoder
$ manim main.py
```

## 15. 오토인코더
" AutoEncoder automatically finds rules in data "
**[[YouTube link](https://www.youtube.com/watch?v=Byo7yew9-OQ)]** <br />
```bash
$ manim autoencoder.py
```

## 16. VAE
" When Autoencoder takes adversity, it become VAE, generative model "
**[[YouTube link](https://www.youtube.com/watch?v=q-n2HNan9jo)]** <br />
Requirements: https://github.com/CodingVillainKor/SimpleDeepLearning/blob/main/vae.ipynb 에서 학습시킨 모델 체크포인트 ae.ckpt, aez1.ckpt
```bash
$ cd vae
$ manim main.py
```

## 17. Diffusion
" Deriving diffusion loss is quite convoluted "
**[[YouTube link](https://www.youtube.com/watch?v=RGlwzCWJubs)]** <br />
```bash
$ manim diffusion1.py
```

## 18. VQVAE1
Vector quantization
**[[YouTube link](https://youtu.be/mypBS6tPPUA)]** <br />
```bash
$ cd vqvae1
$ manim main.py
```

## 19. Neural ODE1
Neural ODE1
**[[YouTube link](https://www.youtube.com/watch?v=afQICWJmpu0)]** <br />
```bash
$ manim node1.py
```

## 20. Neural ODE3
Neural ODE3
**[[YouTube link](https://www.youtube.com/watch?v=UZu2ls-HUlk)]** <br />
```bash
$ manim node3.py
```

## 21. Interior Goat Grazing Problem
Explaining interior goat grazing
**[[YouTube link](https://www.youtube.com/watch?v=feeIKrSsksQ)]** <br />
```bash
$ manim goatgrazing.py
```
