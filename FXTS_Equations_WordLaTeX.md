# Equations in Word Equation-Editor LaTeX (linear) form

All 120 display equations from **FXTS_Delayed_CGBAM_Manuscript**, each ready to
paste into Microsoft Word's equation editor.

**How to use in Word (Microsoft 365 / 2016+):**
1. Insert tab → *Equation* (or press `Alt` `=`).
2. In *Equation Tools → Conversions*, set the input mode to **{} LaTeX**.
3. Paste one equation line below, then press **Enter** (or Space) to render it as a 2-D equation.

> Multi-line systems use `\begin{cases} ... \end{cases}`; coefficient matrices use
> `\begin{bmatrix} ... \end{bmatrix}`. Both are supported by the Word 365 LaTeX converter.
> If your Word build rejects `\mathbb{R}`, replace it with `ℝ` (it renders identically).

---

**Equation (1)**

```latex
\begin{cases} \dot{x}_r(t) = -a_r(x_r(t))[ b_r(x_r(t)) - \sum_{s=1}^{i_2} h_{rs} f_s(y_s(t)) - \sum_{s=1}^{i_2} h_{rs}^{\tau} f_s(y_s(t-\sigma(t))) - I_r ], & t\neq t_\ell, t\in\mathbb{R}^{+} \\ \dot{y}_s(t) = -c_s(y_s(t))[ d_s(y_s(t)) - \sum_{r=1}^{i_1} w_{sr} g_r(x_r(t)) - \sum_{r=1}^{i_1} w_{sr}^{\tau} g_r(x_r(t-\rho(t))) - J_s ], & t\neq t_\ell, t\in\mathbb{R}^{+} \\ \Delta x_r(t_\ell) = \varrho x_r(t_\ell), & \ell\in\mathbb{N} \\ \Delta y_s(t_\ell) = \varsigma y_s(t_\ell), & \ell\in\mathbb{N} \end{cases}
```

**Equation (2)**

```latex
x(t)=(x_1(t),\dots,x_{i_1}(t))^{\top}, y(t)=(y_1(t),\dots,y_{i_2}(t))^{\top},
```

**Equation (3)**

```latex
w(t)=(x^{\top}(t),y^{\top}(t))^{\top}=(w_1(t),\dots,w_{i_1+i_2}(t))^{\top}.
```

**Equation (4)**

```latex
0\le t_0<t_1<t_2<\cdots<t_\ell<\cdots, \lim_{\ell\to+\infty}t_\ell=+\infty,
```

**Equation (5)**

```latex
0\le \sigma(t)\le \tau, 0\le \rho(t)\le \tau, \tau=\sup_{t\ge 0}\max\{\sigma(t),\rho(t)\}<\infty.
```

**Equation (6)**

```latex
0<\hat a_r\le a_r(x)\le \bar a_r, 0<\hat c_s\le c_s(y)\le \bar c_s, \forall x,y\in\mathbb{R}.
```

**Equation (7)**

```latex
0<\hat b_r\le \dot b_r(x)\le \bar b_r, 0<\hat d_s\le \dot d_s(y)\le \bar d_s, \forall x,y\in\mathbb{R}.
```

**Equation (8)**

```latex
|f_s(x)-f_s(y)|\le A_s|x-y|, |g_r(x)-g_r(y)|\le B_r|x-y|, \forall x,y\in\mathbb{R}.
```

**Equation (9)**

```latex
\frac{s-t}{\tau_a}-N_0\leN_\zeta(s,t)\le\frac{s-t}{\tau_a}+N_0, \forall s\ge t\ge 0.
```

**Equation (10)**

```latex
\sum_{k=1}^{i_1+i_2} v_k^{m} \ge (\sum_{k=1}^{i_1+i_2} v_k)^{m},
```

**Equation (11)**

```latex
\sum_{k=1}^{i_1+i_2} v_k^{n} \ge (i_1+i_2)^{1-n}(\sum_{k=1}^{i_1+i_2} v_k)^{n}.
```

**Equation (12)**

```latex
pq \le \frac{\epsilon}{2}p^{2}+\frac{1}{2\epsilon}q^{2}.
```

**Equation (13)**

```latex
W(w(t+\theta)) \le qW(w(t)), \forall\theta\in[-\tau,0],
```

**Equation (14)**

```latex
\begin{cases} \dot{u}(t) = F(u(t),u(t-\tau(t))), & t\neq t_\ell, t\in\mathbb{R}^{+} \\ \Delta u(t_\ell) = J(u(t_\ell)), & \ell\in\mathbb{N} \\ u(\theta) = \varphi(\theta), & \theta\in[-\tau,0] \end{cases}
```

**Equation (15)**

```latex
F(0,0)=0, J(0)=0,
```

**Equation (16)**

```latex
\dot{W}(u(t)) \le -aW^{\alpha}(u(t))-bW^{\beta}(u(t))-cW(u(t)), t\neq t_\ell,
```

**Equation (17)**

```latex
W(u(t_\ell^{+})) \le \xiW(u(t_\ell)), t=t_\ell.
```

**Equation (18)**

```latex
\tau_a > \frac{\ln\xi}{c}.
```

**Equation (19)**

```latex
T=\underbrace{\frac{\ln[1+\frac{(c-\frac{\ln\xi}{\tau_a})}{b\xi^{N_0(1-\beta)}}]}{(c-\frac{\ln\xi}{\tau_a})(\beta-1)}}_{T_1} + \underbrace{\frac{\ln[\frac{a\xi^{-N_0(1-\alpha)}}{\xi^{N_0(1-\alpha)}(c-\frac{\ln\xi}{\tau_a})+a\xi^{-N_0(1-\alpha)}}]}{(\frac{\ln\xi}{\tau_a}-c)(1-\alpha)}}_{T_2},
```

**Equation (20)**

```latex
\begin{cases} \dot{M}(t) = -aM^{\alpha}(t)-cM(t), & 0\le M(t)<1, t\neq t_\ell \\ \dot{M}(t) = -bM^{\beta}(t)-cM(t), & M(t)\ge 1, t\neq t_\ell \\ M(t_\ell^{+}) = \xiM(t_\ell), & t=t_\ell \\ M(0) = W(u(0))=M_0. \end{cases}
```

**Equation (21)**

```latex
0\le W(u(t))\le M(t), t\ge 0,
```

**Equation (22)**

```latex
\begin{cases} \dot{P}(t) = c(\beta-1)P(t)+b(\beta-1), & 0<P(t)\le 1, t\neq t_\ell \\ P(t_\ell^{+}) = \xi_1P(t_\ell), & t=t_\ell \\ P(0) = M_0^{1-\beta} \end{cases}
```

**Equation (23)**

```latex
\begin{cases} \dot{P}(t) = -a(1-\alpha)-c(1-\alpha)P(t), & 0<P(t)<1, t\neq t_\ell \\ P(t_\ell^{+}) = \xi_2P(t_\ell), & t=t_\ell \\ P(0) = 1 \end{cases}
```

**Equation (24)**

```latex
P(t)=e^{c(\beta-1)t}\xi_1^{N_\zeta(t,0)}P(0)+b(\beta-1)\int_0^{t}e^{c(\beta-1)(t-s)}\xi_1^{N_\zeta(t,s)}\mathrm{d}s.
```

**Equation (25)**

```latex
b(\beta-1)e^{c(\beta-1)t}\int_0^{t} e^{-c(\beta-1)s}\xi_1^{(t-s)/\tau_a-N_0}\mathrm{d}s =\frac{e^{[c(\beta-1)+\frac{(\beta-1)\ln\xi_1}{\tau_a}]t}}{\xi_1^{-N_0}b(\beta-1)^{-1}[c(\beta-1)+\frac{(\beta-1)\ln\xi_1}{\tau_a}]},
```

**Equation (26)**

```latex
T_1=\frac{\ln[1+\frac{(c-\frac{\ln\xi}{\tau_a})}{b\xi^{N_0(1-\beta)}}]}{(c-\frac{\ln\xi}{\tau_a})(\beta-1)}.
```

**Equation (27)**

```latex
P(t)=\xi_2^{N_\zeta(t,0)}e^{-c(1-\alpha)t}-a(1-\alpha)\int_0^{t}e^{-c(1-\alpha)(t-s)}\xi_2^{N_\zeta(t,s)}\mathrm{d}s,
```

**Equation (28)**

```latex
T_2=\frac{\ln[\frac{a\xi^{-N_0(1-\alpha)}}{\xi^{N_0(1-\alpha)}(c-\frac{\ln\xi}{\tau_a})+a\xi^{-N_0(1-\alpha)}}]}{(\frac{\ln\xi}{\tau_a}-c)(1-\alpha)}.
```

**Equation (29)**

```latex
\xi:=\max\{|1+\varrho|, |1+\varsigma|\} > 1.
```

**Equation (30)**

```latex
\begin{cases} \dot{u}(t) = -au^{a_1/b_1}(t)-bu^{a_2/b_2}(t)-cu(t), & t\neq t_\ell, t\in\mathbb{R}^{+} \\ u(t_\ell^{+}) = \xiu(t_\ell), & \ell\in\mathbb{N} \end{cases}
```

**Equation (31)**

```latex
\tau_a > \frac{\ln\xi}{c},
```

**Equation (32)**

```latex
T=\frac{\ln[1+\frac{(c-\frac{\ln\xi}{\tau_a})}{b\xi^{N_0\frac{b_2-a_2}{b_2}}}]}{(c-\frac{\ln\xi}{\tau_a})\frac{a_2-b_2}{b_2}} +\frac{\ln[\frac{a\xi^{-N_0\frac{b_1-a_1}{b_1}}}{\xi^{N_0\frac{b_1-a_1}{b_1}}(c-\frac{\ln\xi}{\tau_a})+a\xi^{-N_0\frac{b_1-a_1}{b_1}}}]}{(\frac{\ln\xi}{\tau_a}-c)\frac{b_1-a_1}{b_1}}.
```

**Equation (33)**

```latex
p_r(t)=x_r(t)-x_r^{\ast}, q_s(t)=y_s(t)-y_s^{\ast},
```

**Equation (34)**

```latex
\begin{cases} \tilde a_r(p_r)=a_r(p_r+x_r^{\ast}), & \tilde b_r(p_r)&=b_r(p_r+x_r^{\ast})-b_r(x_r^{\ast}) \\ \tilde c_s(q_s)=c_s(q_s+y_s^{\ast}), & \tilde d_s(q_s)&=d_s(q_s+y_s^{\ast})-d_s(y_s^{\ast}) \\ \tilde f_s(q_s)=f_s(q_s+y_s^{\ast})-f_s(y_s^{\ast}), & \tilde g_r(p_r)&=g_r(p_r+x_r^{\ast})-g_r(x_r^{\ast}). \end{cases}
```

**Equation (35)**

```latex
\begin{cases} \dot p_r(t)=-\tilde a_r(p_r(t))[\tilde b_r(p_r(t))-\sum_{s=1}^{i_2}h_{rs}\tilde f_s(q_s(t))-\sum_{s=1}^{i_2}h_{rs}^{\tau}\tilde f_s(q_s(t-\sigma(t)))], & t\neq t_\ell \\ \dot q_s(t)=-\tilde c_s(q_s(t))[\tilde d_s(q_s(t))-\sum_{r=1}^{i_1}w_{sr}\tilde g_r(p_r(t))-\sum_{r=1}^{i_1}w_{sr}^{\tau}\tilde g_r(p_r(t-\rho(t)))], & t\neq t_\ell \\ \Delta p_r(t_\ell)=\varrhop_r(t_\ell), \Delta q_s(t_\ell)=\varsigmaq_s(t_\ell), & \ell\in\mathbb{N}. \end{cases}
```

**Equation (36)**

```latex
\tilde b_r(p_r(t))=\dot b_r(x_r^{\ast}+\theta_1 p_r(t))p_r(t), \tilde d_s(q_s(t))=\dot d_s(y_s^{\ast}+\theta_2 q_s(t))q_s(t),
```

**Equation (37)**

```latex
|\tilde f_s(q_s)|\le A_s|q_s|, |\tilde g_r(p_r)|\le B_r|p_r|,
```

**Equation (38)**

```latex
\begin{cases} u_r(t)=-k_r^{1}p_r(t)-k_1\mathrm{sign}(p_r(t))|p_r(t)|^{\alpha}-k_2\mathrm{sign}(p_r(t))|p_r(t)|^{\beta} \\ v_s(t)=-m_s^{1}q_s(t)-m_1\mathrm{sign}(q_s(t))|q_s(t)|^{\alpha}-m_2\mathrm{sign}(q_s(t))|q_s(t)|^{\beta} \end{cases}
```

**Equation (39)**

```latex
\begin{cases} \dot p_r(t)=-\tilde a_r(p_r(t))[\tilde b_r(p_r(t))-\sum_{s}h_{rs}\tilde f_s(q_s(t))-\sum_{s}h_{rs}^{\tau}\tilde f_s(q_s(t-\sigma(t)))]+u_r(t), & t\neq t_\ell \\ \dot q_s(t)=-\tilde c_s(q_s(t))[\tilde d_s(q_s(t))-\sum_{r}w_{sr}\tilde g_r(p_r(t))-\sum_{r}w_{sr}^{\tau}\tilde g_r(p_r(t-\rho(t)))]+v_s(t), & t\neq t_\ell \\ \Delta p_r(t_\ell)=\varrhop_r(t_\ell), \Delta q_s(t_\ell)=\varsigmaq_s(t_\ell), & \ell\in\mathbb{N}. \end{cases}
```

**Equation (40)**

```latex
k_r^{1} > \sum_{s=1}^{i_2}\bar c_s B_r|w_{sr}|+q\sum_{s=1}^{i_2}\bar c_s B_r|w_{sr}^{\tau}|-\hat a_r\hat b_r,
```

**Equation (41)**

```latex
m_s^{1} > \sum_{r=1}^{i_1}\bar a_r A_s|h_{rs}|+q\sum_{r=1}^{i_1}\bar a_r A_s|h_{rs}^{\tau}|-\hat c_s\hat d_s.
```

**Equation (42)**

```latex
\tau_a > \frac{\ln\xi}{\delta}, \xi=\max\{|1+\varrho|,|1+\varsigma|\}>1,
```

**Equation (43)**

```latex
T=\frac{\ln[1+\frac{(\delta-\frac{\ln\xi}{\tau_a})}{\tilde\psi\xi^{N_0(1-\beta)}}]}{(\delta-\frac{\ln\xi}{\tau_a})(\beta-1)} +\frac{\ln[\frac{\varphi\xi^{-N_0(1-\alpha)}}{\xi^{N_0(1-\alpha)}(\delta-\frac{\ln\xi}{\tau_a})+\varphi\xi^{-N_0(1-\alpha)}}]}{(\frac{\ln\xi}{\tau_a}-\delta)(1-\alpha)},
```

**Equation (44)**

```latex
W(t)=\sum_{k=1}^{i_1+i_2}|\tilde w_k(t)|=\sum_{r=1}^{i_1}|p_r(t)|+\sum_{s=1}^{i_2}|q_s(t)|.
```

**Equation (45)**

```latex
\dot W(t)=\sum_{r=1}^{i_1}\mathrm{sign}(p_r(t))\dot p_r(t)+\sum_{s=1}^{i_2}\mathrm{sign}(q_s(t))\dot q_s(t).
```

**Equation (46)**

```latex
\begin{cases} \dot W(t)\le &-\sum_{r}\hat a_r\hat b_r|p_r(t)|+\sum_{r}\sum_{s}\bar a_r A_s|h_{rs}||q_s(t)|+\sum_{r}\sum_{s}\bar a_r A_s|h_{rs}^{\tau}||q_s(t-\sigma(t))| \\ &-\sum_{s}\hat c_s\hat d_s|q_s(t)|+\sum_{s}\sum_{r}\bar c_s B_r|w_{sr}||p_r(t)|+\sum_{s}\sum_{r}\bar c_s B_r|w_{sr}^{\tau}||p_r(t-\rho(t))| \\ &-\sum_{r}k_r^{1}|p_r(t)|-\sum_{s}m_s^{1}|q_s(t)|-\varphi\sum_{k}|\tilde w_k(t)|^{\alpha}-\psi\sum_{k}|\tilde w_k(t)|^{\beta} \end{cases}
```

**Equation (47)**

```latex
\dot W(t)\le-\sum_{r}\eta_r|p_r(t)|-\sum_{s}\mu_s|q_s(t)|-\varphi\sum_{k}|\tilde w_k(t)|^{\alpha}-\psi\sum_{k}|\tilde w_k(t)|^{\beta},
```

**Equation (48)**

```latex
\eta_r=k_r^{1}+\hat a_r\hat b_r-\sum_{s}\bar c_s B_r|w_{sr}|-q\sum_{s}\bar c_s B_r|w_{sr}^{\tau}|>0, \mu_s=m_s^{1}+\hat c_s\hat d_s-\sum_{r}\bar a_r A_s|h_{rs}|-q\sum_{r}\bar a_r A_s|h_{rs}^{\tau}|>0.
```

**Equation (49)**

```latex
\dot W(t)\le-\deltaW(t)-\varphiW^{\alpha}(t)-\tilde\psiW^{\beta}(t), \tilde\psi=\psi(i_1+i_2)^{1-\beta}.
```

**Equation (50)**

```latex
W(t_\ell^{+})=\sum_{r}|1+\varrho||p_r(t_\ell)|+\sum_{s}|1+\varsigma||q_s(t_\ell)|\le\xiW(t_\ell), \xi=\max\{|1+\varrho|,|1+\varsigma|\}.
```

**Equation (51)**

```latex
\begin{cases} u_r(t)=-\Phi_rp_r(t)-k_3p_r^{a_1/b_1}(t)-k_4p_r^{a_2/b_2}(t) \\ v_s(t)=-\Psi_sq_s(t)-m_3q_s^{a_1/b_1}(t)-m_4q_s^{a_2/b_2}(t) \end{cases}
```

**Equation (52)**

```latex
\begin{cases} \dot p_r(t)=-\tilde a_r(p_r)[\tilde b_r(p_r)-\sum_s h_{rs}\tilde f_s(q_s)-\sum_s h_{rs}^{\tau}\tilde f_s(q_s(t-\sigma(t)))]+u_r(t) \\ \dot q_s(t)=-\tilde c_s(q_s)[\tilde d_s(q_s)-\sum_r w_{sr}\tilde g_r(p_r)-\sum_r w_{sr}^{\tau}\tilde g_r(p_r(t-\rho(t)))]+v_s(t). \end{cases}
```

**Equation (53)**

```latex
\Phi_r>\sum_{s=1}^{i_2}(\frac{A_s\bar a_r|h_{rs}|\epsilon}{2}+\frac{B_r\bar c_s|w_{sr}|}{2\varepsilon}) +q\sum_{s=1}^{i_2}(\frac{A_s\bar a_r|h_{rs}^{\tau}|\epsilon}{2}+\frac{B_r\bar c_s|w_{sr}^{\tau}|}{2\varepsilon})-\hat a_r\hat b_r,
```

**Equation (54)**

```latex
\Psi_s>\sum_{r=1}^{i_1}(\frac{A_s\bar a_r|h_{rs}|}{2\epsilon}+\frac{B_r\bar c_s|w_{sr}|\varepsilon}{2}) +q\sum_{r=1}^{i_1}(\frac{A_s\bar a_r|h_{rs}^{\tau}|}{2\epsilon}+\frac{B_r\bar c_s|w_{sr}^{\tau}|\varepsilon}{2})-\hat c_s\hat d_s.
```

**Equation (55)**

```latex
\tau_a>\frac{\ln\tilde\xi}{\tilde\Theta}, \tilde\xi=\max\{(1+\varrho)^2,(1+\varsigma)^2\}>1,
```

**Equation (56)**

```latex
T=\frac{\ln[1+\frac{(\tilde\Theta-\frac{\ln\tilde\xi}{\tau_a})}{\tilde\rho\tilde\xi^{N_0(1-\beta)}}]}{(\tilde\Theta-\frac{\ln\tilde\xi}{\tau_a})(\beta-1)} +\frac{\ln[\frac{\tilde\chi\tilde\xi^{-N_0(1-\alpha)}}{\tilde\xi^{N_0(1-\alpha)}(\tilde\Theta-\frac{\ln\tilde\xi}{\tau_a})+\tilde\chi\tilde\xi^{-N_0(1-\alpha)}}]}{(\frac{\ln\tilde\xi}{\tau_a}-\tilde\Theta)(1-\alpha)},
```

**Equation (57)**

```latex
W(t)=\frac12\sum_{k=1}^{i_1+i_2}\tilde w_k^{2}(t)=\frac12\sum_{r}p_r^{2}(t)+\frac12\sum_{s}q_s^{2}(t).
```

**Equation (58)**

```latex
\dot W(t)=\sum_{r}p_r(t)\dot p_r(t)+\sum_{s}q_s(t)\dot q_s(t).
```

**Equation (59)**

```latex
\begin{cases} \dot W(t)\le &-\sum_{r}\hat a_r\hat b_r p_r^{2}+\sum_{r}\sum_{s}(\frac{A_s\bar a_r|h_{rs}|\epsilon}{2}+q\frac{A_s\bar a_r|h_{rs}^{\tau}|\epsilon}{2})p_r^{2}+\sum_{s}\sum_{r}(\frac{B_r\bar c_s|w_{sr}|}{2\varepsilon}+q\frac{B_r\bar c_s|w_{sr}^{\tau}|}{2\varepsilon})p_r^{2} \\ &-\sum_{s}\hat c_s\hat d_s q_s^{2}+\text{(symmetric $q_s^{2}$ cross terms)}-\sum_{r}\Phi_r p_r^{2}-\sum_{s}\Psi_s q_s^{2} \\ &-k_3\sum_r p_r^{\frac{a_1+b_1}{b_1}}-k_4\sum_r p_r^{\frac{a_2+b_2}{b_2}}-m_3\sum_s q_s^{\frac{a_1+b_1}{b_1}}-m_4\sum_s q_s^{\frac{a_2+b_2}{b_2}}. \end{cases}
```

**Equation (60)**

```latex
\dot W(t)\le-\sum_{r}\gamma_r p_r^{2}-\sum_{s}\lambda_s q_s^{2}-k_3\sum_r p_r^{\frac{a_1+b_1}{b_1}}-k_4\sum_r p_r^{\frac{a_2+b_2}{b_2}}-m_3\sum_s q_s^{\frac{a_1+b_1}{b_1}}-m_4\sum_s q_s^{\frac{a_2+b_2}{b_2}},
```

**Equation (61)**

```latex
\gamma_r=\Phi_r+\hat a_r\hat b_r-\sum_{s}(\frac{A_s\bar a_r|h_{rs}|\epsilon}{2}+\frac{B_r\bar c_s|w_{sr}|}{2\varepsilon})-q\sum_{s}(\frac{A_s\bar a_r|h_{rs}^{\tau}|\epsilon}{2}+\frac{B_r\bar c_s|w_{sr}^{\tau}|}{2\varepsilon})>0,
```

**Equation (62)**

```latex
\dot W(t)\le-\tilde\ThetaW(t)-\tilde\chiW^{\frac{a_1+b_1}{2b_1}}(t)-\tilde\rhoW^{\frac{a_2+b_2}{2b_2}}(t),
```

**Equation (63)**

```latex
W(t_\ell^{+})=\frac12\sum_{r}(1+\varrho)^2 p_r^{2}(t_\ell)+\frac12\sum_{s}(1+\varsigma)^2 q_s^{2}(t_\ell)\le\tilde\xiW(t_\ell), \tilde\xi=\max\{(1+\varrho)^2,(1+\varsigma)^2\}.
```

**Equation (64)**

```latex
\begin{cases} \dot x_1(t)=0.1\sin(x_2(t))+0.05\sin(x_2(t-\sigma(t)))+u_1(t), & t\neq t_\ell \\ \dot x_2(t)=0.1\sin(x_1(t))+0.05\sin(x_1(t-\sigma(t)))+u_2(t), & t\neq t_\ell \\ x_i(t_\ell^{+})=\xix_i(t_\ell), i=1,2, & t=t_\ell \end{cases}
```

**Equation (65)**

```latex
u_i(t)=-0.5x_i(t)-0.4\mathrm{sign}(x_i(t))|x_i(t)|^{0.5}-1.2\mathrm{sign}(x_i(t))|x_i(t)|^{1.5}, i=1,2.
```

**Equation (66)**

```latex
t_\ell-t_{\ell-1}= \begin{cases} h, & \operatorname{mod}(\ell,N_0)\neq 0,\\ N_0(\tau_a-h)+h, & \operatorname{mod}(\ell,N_0)=0, \end{cases}
```

**Equation (67)**

```latex
W(t)=|x_1(t)|+|x_2(t)|,
```

**Equation (68)**

```latex
\dot W(t)\le-0.5W(t)+0.1W(t)+0.05W(t-\sigma(t))-0.4(|x_1|^{0.5}+|x_2|^{0.5})-1.2(|x_1|^{1.5}+|x_2|^{1.5}).
```

**Equation (69)**

```latex
\dot W(t)\le-0.34W(t)-0.4W^{0.5}(t)-0.8485W^{1.5}(t),
```

**Equation (70)**

```latex
W(t_\ell^{+})=\xiW(t_\ell), \xi=1.2.
```

**Equation (71)**

```latex
\tau_a>\frac{\ln\xi}{c}=\frac{\ln 1.2}{0.34}=0.536.
```

**Equation (72)**

```latex
T_{\text{est}}=T_1+T_2\approx 2.55+5.70=8.26.
```

**Equation (73)**

```latex
\tau_a=0.1<0.536, N_0=2, h=0.02,
```

**Equation (74)**

```latex
\begin{cases} \dot x_r(t)=-a_r(x_r)[b_r(x_r)-\sum_{s=1}^{2}h_{rs}f_s(y_s(t))-\sum_{s=1}^{2}h_{rs}^{\tau}f_s(y_s(t-\sigma(t)))-I_r]+u_r(t) \\ \dot y_s(t)=-c_s(y_s)[d_s(y_s)-\sum_{r=1}^{2}w_{sr}g_r(x_r(t))-\sum_{r=1}^{2}w_{sr}^{\tau}g_r(x_r(t-\rho(t)))-J_s]+v_s(t) \end{cases}
```

**Equation (75)**

```latex
a_1(x_1)=0.8+\frac{0.2}{1+x_1^{2}}, a_2(x_2)=0.6+\frac{0.3}{1+x_2^{2}},
```

**Equation (76)**

```latex
c_1(y_1)=1.4+\frac{0.6}{1+y_1^{2}}, c_2(y_2)=0.74+\frac{0.6}{1+y_2^{2}},
```

**Equation (77)**

```latex
b_1(x_1)=0.5x_1, b_2(x_2)=0.74x_2, d_1(y_1)=0.2y_1, d_2(y_2)=0.3y_2,
```

**Equation (78)**

```latex
[h_{rs}]=\begin{bmatrix}2.5&0.5\\0.3&1.5\end{bmatrix}, [w_{sr}]=\begin{bmatrix}-0.4&1.3\\1.5&-0.4\end{bmatrix},
```

**Equation (79)**

```latex
[h_{rs}^{\tau}]=\begin{bmatrix}0.5&0.1\\0.06&0.3\end{bmatrix}, [w_{sr}^{\tau}]=\begin{bmatrix}-0.08&0.26\\0.3&-0.08\end{bmatrix}.
```

**Equation (80)**

```latex
g_r(x)=0.5\tanh(x), f_s(y)=0.5(|y+1|-|y-1|),
```

**Equation (81)**

```latex
0.8\le a_1\le 1, 0.6\le a_2\le 0.9, 1.4\le c_1\le 2, 0.74\le c_2\le 1.34,
```

**Equation (82)**

```latex
\hat b_1=\bar b_1=0.5, \hat b_2=\bar b_2=0.74, \hat d_1=0.2, \hat d_2=0.3.
```

**Equation (83)**

```latex
k_1^{1}>3.084, k_2^{1}>3.445,
```

**Equation (84)**

```latex
m_1^{1}>3.155, m_2^{1}>2.072.
```

**Equation (85)**

```latex
\eta_1=0.916, \eta_2=0.555, \mu_1=0.845, \mu_2=1.928, \delta=\min=0.555,
```

**Equation (86)**

```latex
\varphi=\min\{k_1,m_1\}=1.25, \tilde\psi=\psi(i_1+i_2)^{1-\beta}=4\cdot 4^{-0.8}=1.319.
```

**Equation (87)**

```latex
\tau_a>\frac{\ln\xi}{\delta}=\frac{\ln 1.1}{0.555}=0.172.
```

**Equation (88)**

```latex
T_{\text{est}}\approx 0.93+3.66=4.60.
```

**Equation (89)**

```latex
\Phi_1>4.014, \Phi_2>3.541,
```

**Equation (90)**

```latex
\Psi_1>4.209, \Psi_2>2.487.
```

**Equation (91)**

```latex
\gamma_1=1.986, \gamma_2=2.053, \lambda_1=1.791, \lambda_2=3.139, \Theta=\min=1.791,
```

**Equation (92)**

```latex
\tilde\Theta=2\Theta=3.582, \tilde\chi=0.5\cdot 2^{5/7}=0.820, \tilde\rho=1.5\cdot 2^{1.4}\cdot 4^{-0.4}=2.273.
```

**Equation (93)**

```latex
\tau_a>\frac{\ln\tilde\xi}{\tilde\Theta}=\frac{\ln 1.44}{3.582}=0.102.
```

**Equation (94)**

```latex
T_{\text{est}}\approx 0.79+2.04=2.83.
```

**Equation (95)**

```latex
u_r(t)=-k_3 p_r^{a_1/b_1}(t)-k_4 p_r^{a_2/b_2}(t), v_s(t)=-m_3 q_s^{a_1/b_1}(t)-m_4 q_s^{a_2/b_2}(t),
```

**Equation (96)**

```latex
\dot W(t)\le-\tilde\chiW^{\alpha}(t)-\tilde\rhoW^{\beta}(t).
```

**Equation (97)**

```latex
\kappa:=c-\frac{\ln\xi}{\tau_a}=0.34-0.18232=0.15768,
```

**Equation (98)**

```latex
\xi^{N_0(1-\beta)}=1.2^{2(1-1.5)}=0.8333,
```

**Equation (99)**

```latex
T_1=\frac{\ln[1+\kappa/(b\xi^{N_0(1-\beta)})]}{\kappa(\beta-1)}=\frac{\ln(1.2230)}{0.15768\cdot 0.5}=2.553,
```

**Equation (100)**

```latex
\xi^{-N_0(1-\alpha)}=0.8333, \xi^{N_0(1-\alpha)}=1.2,
```

**Equation (101)**

```latex
T_2=\frac{\ln[a\xi^{-N_0(1-\alpha)}/(\xi^{N_0(1-\alpha)}\kappa+a\xi^{-N_0(1-\alpha)})]}{(-\kappa)(1-\alpha)}=\frac{\ln(0.6379)}{-0.07884}=5.703,
```

**Equation (102)**

```latex
T_{\text{est}}=T_1+T_2=8.256.
```

**Equation (103)**

```latex
\kappa=\delta-\frac{\ln\xi}{\tau_a}=0.555-0.11914=0.43586,
```

**Equation (104)**

```latex
T_1=\frac{\ln[1+\kappa/(\tilde\psi\xi^{N_0(1-\beta)})]}{\kappa(\beta-1)}=\frac{\ln(1.3850)}{0.43586\cdot 0.8}=0.934,
```

**Equation (105)**

```latex
T_2=\frac{\ln[\varphi\xi^{-N_0(1-\alpha)}/(\xi^{N_0(1-\alpha)}\kappa+\varphi\xi^{-N_0(1-\alpha)})]}{(-\kappa)(1-\alpha)}=\frac{\ln(0.7265)}{-0.08717}=3.664,
```

**Equation (106)**

```latex
T_{\text{est}}=T_1+T_2=4.598.
```

**Equation (107)**

```latex
\kappa=\tilde\Theta-\frac{\ln\tilde\xi}{\tau_a}=3.582-0.72928=2.85272,
```

**Equation (108)**

```latex
T_1=\frac{\ln[1+\kappa/(\tilde\rho\tilde\xi^{N_0(1-\beta)})]}{\kappa(\beta-1)}=\frac{\ln(2.4519)}{2.85272\cdot 0.4}=0.786,
```

**Equation (109)**

```latex
T_2=\frac{\ln[\tilde\chi\tilde\xi^{-N_0(1-\alpha)}/(\tilde\xi^{N_0(1-\alpha)}\kappa+\tilde\chi\tilde\xi^{-N_0(1-\alpha)})]}{(-\kappa)(1-\alpha)}=\frac{\ln(0.1892)}{-0.81506}=2.042,
```

**Equation (110)**

```latex
T_{\text{est}}=T_1+T_2=2.828.
```

**Equation (111)**

```latex
\kappa(\tau_a)=c-\frac{\ln\xi}{\tau_a}, \tau_a>\frac{\ln\xi}{c}.
```

**Equation (112)**

```latex
\frac{\mathrm{d}\kappa}{\mathrm{d}\tau_a}=\frac{\ln\xi}{\tau_a^{2}}>0,
```

**Equation (113)**

```latex
\frac{\mathrm{d}T_{\text{est}}}{\mathrm{d}\tau_a}<0,
```

**Equation (114)**

```latex
\lim_{\tau_a\to(\ln\xi/c)^{+}}\kappa(\tau_a)=0^{+} \Longrightarrow \lim_{\tau_a\to(\ln\xi/c)^{+}}T_{\text{est}}=+\infty,
```

**Equation (115)**

```latex
\lim_{\tau_a\to\infty}\kappa(\tau_a)=c \Longrightarrow \lim_{\tau_a\to\infty}T_{\text{est}}=T_\infty,
```

**Equation (116)**

```latex
T_\infty=\frac{1}{c(\beta-1)}\ln(1+\frac{c}{b})+\frac{1}{c(1-\alpha)}\ln(\frac{c+a}{a}).
```

**Equation (117)**

```latex
T_\infty=\frac{\ln(1.4007)}{0.17}+\frac{\ln(1.85)}{0.17}=1.982+3.619=5.601,
```

**Equation (118)**

```latex
T_{\text{obs}}\le T_{\text{est}}: 1.10\le 8.26, 0.68\le 4.60, 0.58\le 2.83,
```

**Equation (119)**

```latex
r:=\frac{T_{\text{obs}}}{T_{\text{est}}}\in\{0.133, 0.148, 0.205\},
```

**Equation (120)**

```latex
\frac{\tau_a}{\ln\xi/c}>1: \frac{1}{0.536}=1.87, \frac{0.8}{0.172}=4.65, \frac{0.5}{0.102}=4.90.
```
