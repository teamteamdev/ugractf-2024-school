# Late Stage Capitalism: Write-up

Посмотрим, что приложено к заданию.

Во-первых, есть сайт, где можно купить **UCUCUGA PRO EDITION** за целый 1 BTC. При этом указан адрес, на который надо перевести деньги. Адреса Bitcoin содержат в себе контрольную сумму; у данного адреса контрольная сумма не сходится, поэтому по-честному купить уцуцугу не получится.

Также есть кнопка для получения уцуцуги по ключу. В коде страницы видим, что эта кнопка обрабатывается следующим образом:

```javascript
async function have() {
    const key = prompt("Введите ключ активации:");
    alert(await (await fetch(`get-flag/${key}`)).text());
}
```

Таким образом, чтобы получить флаг, нам просто нужно узнать ключ активации. Запомним это.

---

Теперь посмотрим на программу `keygen`. После запуска и ввода токена видим:

```
UCUCUGA PRO KEYGEN by xXx_HACKERNAME_xXx
Enter token: maziserywq8vln9u
You need to obtain a key from me to use this keygen.
Please mail purplesyringa@example.com. We will agree on the payment.
Enter key from purplesyringa: 
```

Ага, понятно. Чтобы получить ключ к уцуцуге, нужно сначала получить ключ к кейгену. На это указывает и фраза «Другое дело, что хакерам тоже хочется кушать» из условия задачи.

---

Будем реверсить `keygen`. Воспользуемся для этого IDA Free (ближе к концу соревнования она была приложена к заданию; до этого можно было использовать свою копию, если она была в образе виртуальной машины, либо найти альтернативный способ её скачать). Задание также можно решить с помощью Ghidra.

Декомпилируем `main` (нажатием F5):

```c
// local variable allocation has failed, the output may be wrong!
int __fastcall __noreturn main(int argc, const char **argv, const char **envp)
{
  char **v3; // rdx

  __shedskin__::__init(*(__shedskin__ **)&argc);
  __sys__::__init((__sys__ *)(unsigned int)argc, (int)argv, v3);
  __shedskin__::__start((__shedskin__ *)__keygen__::__init, (void (*)(void))argv);
}
```

Сразу натыкаемся на интересное название пространства имён `__shedskin__`. Загуглим *shedskin*. Оказывается, что это транслятор Python в C++, который затем был скомпилирован в бинарный код, к счастью, с символами.

Судя по всему, `__init` инициализирует рантайм, так что заглянем внутри функции `__start`. Она не содержит ничего особо интересного, но вызывает первый аргумент:

```c
void __fastcall __noreturn __shedskin__::__start(__shedskin__ *this, void (*a2)(void))
{
  std::set_terminate((void (*)(void))__shedskin__::terminate_handler);
  ((void (__fastcall *)(void (__fastcall __noreturn *)(__shedskin__ *__hidden), void (*)(void)))this)(
    __shedskin__::terminate_handler,
    a2);
  exit(0);
}
```

Значит, заглянем в `__keygen__::__init__`:

```c
__int64 __fastcall __keygen__::__init(__keygen__ *this)
{
  __shedskin__::str *v1; // rax
  __shedskin__::str *v2; // rbx
  __shedskin__::str *v3; // rax
  __shedskin__ *v4; // rbx
  __shedskin__::str *v5; // rax
  __int64 v6; // rbx
  __shedskin__::str *v7; // rax
  __int64 v8; // rbx
  __shedskin__::str *v9; // rax
  __int64 v10; // rbx
  __shedskin__::str *v11; // rax
  __int64 v12; // rbx
  __shedskin__::str *v13; // rax
  __int64 v14; // rbx
  __shedskin__::str *v15; // rax
  __int64 v16; // rbx
  __shedskin__::str *v17; // rax
  __int64 v18; // rbx
  __shedskin__::str *v19; // rax
  __shedskin__::str *v20; // rbx
  __shedskin__::str *v21; // rax
  __int64 v22; // rbx
  __shedskin__::str *v23; // rax
  __int64 v24; // rbx
  __keygen__ *v25; // rdi

  v1 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v2 = v1;
  if ( !v1 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v1, "0123456789abcdef");
  __keygen__::const_0 = v2;
  v3 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v4 = v3;
  if ( !v3 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v3, "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-");
  __keygen__::const_1 = v4;
  v5 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v6 = (__int64)v5;
  if ( !v5 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v5, &path);
  __keygen__::const_2 = v6;
  v7 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v8 = (__int64)v7;
  if ( !v7 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v7, "Invalid hex format");
  __keygen__::const_3 = v8;
  v9 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v10 = (__int64)v9;
  if ( !v9 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v9, "UCUCUGA PRO KEYGEN by xXx_HACKERNAME_xXx");
  __keygen__::const_4 = v10;
  v11 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v12 = (__int64)v11;
  if ( !v11 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v11, "Enter token: ");
  __keygen__::const_5 = v12;
  v13 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v14 = (__int64)v13;
  if ( !v13 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v13, "You need to obtain a key from me to use this keygen.");
  __keygen__::const_6 = v14;
  v15 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v16 = (__int64)v15;
  if ( !v15 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v15, "Please mail purplesyringa@example.com. We will agree on the payment.");
  __keygen__::const_7 = v16;
  v17 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v18 = (__int64)v17;
  if ( !v17 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v17, "Enter key from purplesyringa: ");
  __keygen__::const_8 = v18;
  v19 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v20 = v19;
  if ( !v19 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v19, "UCUCUGA Pro key: ");
  __keygen__::const_9 = v20;
  v21 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v22 = (__int64)v21;
  if ( !v21 )
    GC_throw_bad_alloc();
  __shedskin__::str::str(v21, "The key is invalid.");
  __keygen__::const_10 = v22;
  v23 = (__shedskin__::str *)GC_malloc(0x40uLL);
  v24 = (__int64)v23;
  if ( !v23 )
    GC_throw_bad_alloc();
  v25 = v23;
  __shedskin__::str::str(v23, "__main__");
  __keygen__::__name__ = v24;
  return __keygen__::__ss_main(v25);
}
```

Здесь, по-видимому, преаллоцируются строки, а затем запускается функция `__ss_main`. Откроем её:

```c
__int64 __fastcall __keygen__::__ss_main(__keygen__ *this)
{
  __shedskin__ *v1; // rbp
  __keygen__ *v2; // rax
  __int64 *v3; // r12
  _QWORD *v4; // rax
  __int64 v5; // rcx
  _QWORD *v6; // rbx
  __int64 v7; // rax
  __int64 v8; // rax
  __int64 (__fastcall *v9)(); // rax
  __int64 v10; // rax
  __int64 v11; // rdx
  __int64 v12; // rdx
  __int64 v13; // rcx
  char v14; // al
  __int64 v15; // r8
  __shedskin__::str *ucucuga_key; // rax
  __int64 v18; // [rsp+8h] [rbp-20h]

  __shedskin__::print<__shedskin__::str *>((unsigned __int8)__shedskin__::False, 0LL, 0LL, 0LL, __keygen__::const_4);
  __shedskin__::print<__shedskin__::str *>(
    (unsigned __int8)__shedskin__::False,
    0LL,
    __keygen__::const_2,
    0LL,
    __keygen__::const_5);
  (*(void (__fastcall **)(__int64))(*(_QWORD *)__sys__::__ss_stdout + 168LL))(__sys__::__ss_stdout);
  v1 = (__shedskin__ *)__shedskin__::input(0LL, 0LL);
  __shedskin__::print<__shedskin__::str *>((unsigned __int8)__shedskin__::False, 0LL, 0LL, 0LL, __keygen__::const_6);
  __shedskin__::print<__shedskin__::str *>((unsigned __int8)__shedskin__::False, 0LL, 0LL, 0LL, __keygen__::const_7);
  __shedskin__::print<__shedskin__::str *>(
    (unsigned __int8)__shedskin__::False,
    0LL,
    __keygen__::const_2,
    0LL,
    __keygen__::const_8);
  (*(void (__fastcall **)(__int64))(*(_QWORD *)__sys__::__ss_stdout + 168LL))(__sys__::__ss_stdout);
  v2 = (__keygen__ *)__shedskin__::input(0LL, 0LL);
  v3 = (__int64 *)__keygen__::parse_hex(v2, 0LL);
  v4 = GC_malloc(0x28uLL);
  v6 = v4;
  if ( !v4 )
    GC_throw_bad_alloc();
  v4[2] = 0LL;
  *v4 = &off_5468E0;
  v7 = __shedskin__::cl_list;
  v6[3] = 0LL;
  v6[1] = v7;
  v8 = *v3;
  v6[4] = 0LL;
  v9 = *(__int64 (__fastcall **)())(v8 + 96);
  if ( v9 == __shedskin__::list<int>::__len__ )
    v10 = (v3[3] - v3[2]) >> 2;
  else
    LODWORD(v10) = ((__int64 (__fastcall *)(__int64 *))v9)(v3);
  v11 = (int)v10;
  if ( (int)v10 > 0 || (v5 = 0LL, (_DWORD)v10) )
  {
    v18 = (int)v10;
    std::vector<int,gc_allocator<int>>::_M_default_append(v6 + 2, (int)v10, (int)v10, v5);
    v5 = v6[2];
    v11 = 4 * v18;
  }
  v13 = _memcpy_fwd(v5, v3[2], v11);
  if ( (unsigned int)((v6[3] - v13) >> 2) == 16 )
    v14 = __keygen__::validate_purplesyringa_key(v1);
  else
    v14 = __shedskin__::False;
  v15 = __keygen__::const_10;
  if ( v14 )
  {
    ucucuga_key = (__shedskin__::str *)__keygen__::generate_ucucuga_key(v1, v3, v12, v13, __keygen__::const_10);
    v15 = __shedskin__::str::__add__(__keygen__::const_9, ucucuga_key);
  }
  __shedskin__::print<__shedskin__::str *>((unsigned __int8)__shedskin__::False, 0LL, 0LL, 0LL, v15);
  return 0LL;
}
```

Постараемся проигнорировать весь мусор и предположим по вызовам функций, как это выглядело бы в коде на Python. Единственная нетривиальная часть — догадаться по девиртуализованному вызову `list::__len__`, что значения по индексам 2 и 3 у списка содержат адресы начала и конца массива соответственно.

```python
def main():
    print(???)
    print(???)
    sys.stdout.???()
    v1 = input()
    print(???)
    print(???)
    print(???)
    sys.stdout.???()
    v2 = input()
    v3 = parse_hex(v2)
    v6 = list(v3)
    if len(v6) == 16:
        v14 = validate_purplesyringa_key(v1)
    else:
        v14 = False
    v15 = ???
    if v14:
        ucucuga_key = generate_ucucuga_key(v1, v3);
        v15 = ??? + ucucuga_key
    print(v15)
```

Итак, сначала токен вводится в `v1`, затем ключ от кейгена считывается как hex в `v3`, проверяется, что он занимает 16 байт и `validate_purplesyringa_key` выдает `True`, и в случае успеха вызывается `generate_ucucuga_key`. Единственная странность заключается в том, что `validate_purplesyringa_key` принимает на вход только *токен*, а не только что считанный в `v6` ключ.

Ну ничего, откроем `validate_purplesyringa_key`:

```c
__int64 __fastcall __keygen__::validate_purplesyringa_key(__shedskin__ *this, __int64 a2)
{
  __int64 v2; // r12
  __shedskin__ *v3; // rbp
  __int64 v5; // rcx
  __int64 v6; // rsi
  __int64 v7; // rdx
  int *v8; // rax
  int v9; // r13d
  __int64 v10; // r14
  __int64 i; // r13
  __int64 v12; // r14
  int v13; // eax
  bool v14; // sf
  int v15; // r12d
  int v16; // eax
  int v17; // ecx
  int v18; // r15d
  int j; // r14d
  signed int v20; // eax
  signed int v21; // r12d
  int v22; // r13d
  __int64 v23; // r12
  int v24; // ecx
  __int64 v25; // r14
  int v26; // r15d
  __int64 (__fastcall *v27)(__shedskin__::str *__hidden); // rax

  v2 = 0LL;
  v3 = this;
  v5 = *(_QWORD *)(a2 + 16);
  v6 = *(_QWORD *)(a2 + 24);
  v7 = v5;
  do
  {
    v10 = 4 * v2;
    if ( (int)v2 >= (int)((v6 - v5) >> 2) )
      __shedskin__::__throw_index_out_of_range(this);
    v8 = (int *)(v5 + v10);
    v9 = *(_DWORD *)(v5 + 4 * v2);
    if ( !v9 )
    {
      v9 = 256;
      v7 = v5;
      v8 = (int *)(v5 + v10);
    }
    ++v2;
    *v8 = v9;
  }
  while ( v2 != 16 );
  for ( i = 0LL; i != 15; ++i )
  {
    v17 = (v6 - v7) >> 2;
    if ( v17 <= (int)i + 1 )
      __shedskin__::__throw_index_out_of_range(this);
    v12 = 4 * i;
    if ( v17 <= (int)i )
      __shedskin__::__throw_index_out_of_range(this);
    v13 = *(_DWORD *)(v7 + 4 * i) * *(_DWORD *)(v7 + 4 * i + 4);
    this = (__shedskin__ *)(unsigned int)(257 * (v13 / 257));
    v13 %= 257;
    v14 = v13 < 0;
    v15 = v13;
    v16 = v13 + 257;
    if ( v14 )
      v15 = v16;
    if ( (int)i + 1 >= v17 )
      __shedskin__::__throw_index_out_of_range(this);
    *(_DWORD *)(v7 + v12 + 4) = v15;
  }
  v18 = 433;
  for ( j = 743893; j != 743893000; j += 743893 )
  {
    v22 = (j >> 16) & 0xF;
    v23 = (v18 >> 4) & 0xF;
    if ( v22 != (_DWORD)v23 )
    {
      v24 = (v6 - v7) >> 2;
      if ( v22 >= v24 )
        __shedskin__::__throw_index_out_of_range(this);
      this = (__shedskin__ *)v22;
      if ( (int)v23 >= v24 )
        __shedskin__::__throw_index_out_of_range((__shedskin__ *)v22);
      v20 = (unsigned __int8)(((unsigned int)((*(_DWORD *)(v7 + 4 * v23) + *(_DWORD *)(v7 + 4LL * v22)) >> 31) >> 24)
                            + *(_BYTE *)(v7 + 4 * v23)
                            + *(_DWORD *)(v7 + 4LL * v22))
          - ((unsigned int)((*(_DWORD *)(v7 + 4 * v23) + *(_DWORD *)(v7 + 4LL * v22)) >> 31) >> 24);
      v21 = v20 + 256;
      if ( v20 >= 0 )
        v21 = v20;
      if ( v22 >= v24 )
        __shedskin__::__throw_index_out_of_range((__shedskin__ *)v22);
      *(_DWORD *)(v7 + 4LL * v22) = v21;
    }
    v18 += 433;
  }
  v25 = 0LL;
  while ( 1 )
  {
    if ( (int)v25 >= (int)((v6 - v7) >> 2) )
      __shedskin__::__throw_index_out_of_range(this);
    v26 = *(_DWORD *)(v7 + 4 * v25);
    v27 = *(__int64 (__fastcall **)(__shedskin__::str *__hidden))(*(_QWORD *)v3 + 96LL);
    if ( v27 == __shedskin__::str::__len__ )
    {
      if ( (int)v25 >= *((_DWORD *)v3 + 6) )
        goto LABEL_38;
    }
    else
    {
      this = v3;
      if ( (int)v25 >= (int)v27(v3) )
LABEL_38:
        __shedskin__::__throw_index_out_of_range(this);
    }
    this = *(__shedskin__ **)(__shedskin__::__char_cache + 8LL * *(unsigned __int8 *)(*((_QWORD *)v3 + 2) + v25));
    if ( *((_QWORD *)this + 3) != 1LL )
      __keygen__::validate_purplesyringa_key();
    if ( *(unsigned __int8 *)__shedskin__::str::c_str(this) != v26 )
      return (unsigned __int8)__shedskin__::False;
    if ( ++v25 == 16 )
      return (unsigned __int8)__shedskin__::True;
    v6 = *(_QWORD *)(a2 + 24);
    v7 = *(_QWORD *)(a2 + 16);
  }
}
```

Пролистаем код. Бросается в глаза запись в `this`. По-видимому, это на самом деле не `this`, и IDA неправильно предположила, что функция — метод класса. На самом деле, если посмотреть на mangled имя функции, мы увидим:

```
_ZN10__keygen__26validate_purplesyringa_keyEPN12__shedskin__3strEPNS0_4listIiEE.part.0
```

То есть функция принимает `__shedskin__::str *` и `__shedskin__::list<int> *`, а не те типы, которые вывела IDA. Переименуем `this` в `token`, `a2` — в `purplesyringa_key`. Опираясь на знание о том, что `(v6 - v5) >> 2)` — скорее всего, вычисление размера массива, создадим из списка структуру с полями-указателями `int *start, *end;`.

После этого код становится более читабельным, и можно немного переименовать переменные:

```c
__int64 __fastcall __keygen__::validate_purplesyringa_key(__shedskin__::str *token, list_int *purplesyringa_key)
{
  __int64 i_1; // r12
  struct_v3 *v3; // rbp
  int *start1; // rcx
  int *end1; // rsi
  int *start; // rdx
  int *v8; // rax
  int v9; // r13d
  __int64 offset; // r14
  __int64 i; // r13
  __int64 v12; // r14
  int x; // eax
  bool is_negative; // sf
  int v15; // r12d
  int v16; // eax
  int length; // ecx
  int v18; // r15d
  int j; // r14d
  signed int x_1; // eax
  signed int v21; // r12d
  int i_2; // r13d
  __int64 j_1; // r12
  int length_1; // ecx
  __int64 i_3; // r14
  int v26; // r15d
  __int64 (__fastcall *length_getter)(__shedskin__::str *__hidden); // rax

  i_1 = 0LL;
  v3 = (struct_v3 *)token;
  start1 = purplesyringa_key->start;
  end1 = purplesyringa_key->end;
  start = start1;
  do
  {
    offset = i_1;
    if ( (int)i_1 >= (int)(end1 - start1) )
      __shedskin__::__throw_index_out_of_range(token);
    v8 = &start1[offset];
    v9 = start1[i_1];
    if ( !v9 )
    {
      v9 = 256;
      start = start1;
      v8 = &start1[offset];
    }
    ++i_1;
    *v8 = v9;
  }
  while ( i_1 != 16 );
  for ( i = 0LL; i != 15; ++i )
  {
    length = end1 - start;
    if ( length <= (int)i + 1 )
      __shedskin__::__throw_index_out_of_range(token);
    v12 = i;
    if ( length <= (int)i )
      __shedskin__::__throw_index_out_of_range(token);
    x = start[i] * start[i + 1];
    token = (__shedskin__::str *)(unsigned int)(257 * (x / 257));
    x %= 257;
    is_negative = x < 0;
    v15 = x;
    v16 = x + 257;
    if ( is_negative )
      v15 = v16;
    if ( (int)i + 1 >= length )
      __shedskin__::__throw_index_out_of_range(token);
    start[v12 + 1] = v15;
  }
  v18 = 433;
  for ( j = 743893; j != 743893000; j += 743893 )
  {
    i_2 = (j >> 16) & 0xF;
    j_1 = (v18 >> 4) & 0xF;
    if ( i_2 != (_DWORD)j_1 )
    {
      length_1 = end1 - start;
      if ( i_2 >= length_1 )
        __shedskin__::__throw_index_out_of_range(token);
      token = (__shedskin__::str *)i_2;
      if ( (int)j_1 >= length_1 )
        __shedskin__::__throw_index_out_of_range((__shedskin__ *)i_2);
      x_1 = (unsigned __int8)(((unsigned int)((start[j_1] + start[i_2]) >> 31) >> 24) + LOBYTE(start[j_1]) + start[i_2])
          - ((unsigned int)((start[j_1] + start[i_2]) >> 31) >> 24);
      v21 = x_1 + 256;
      if ( x_1 >= 0 )
        v21 = x_1;
      if ( i_2 >= length_1 )
        __shedskin__::__throw_index_out_of_range((__shedskin__ *)i_2);
      start[i_2] = v21;
    }
    v18 += 433;
  }
  i_3 = 0LL;
  while ( 1 )
  {
    if ( (int)i_3 >= (int)(end1 - start) )
      __shedskin__::__throw_index_out_of_range(token);
    v26 = start[i_3];
    length_getter = *(__int64 (__fastcall **)(__shedskin__::str *__hidden))(v3->qword0 + 96LL);
    if ( length_getter == __shedskin__::str::__len__ )
    {
      if ( (int)i_3 >= v3->length )
        goto LABEL_38;
    }
    else
    {
      token = (__shedskin__::str *)v3;
      if ( (int)i_3 >= (int)length_getter((__shedskin__::str *)v3) )
LABEL_38:
        __shedskin__::__throw_index_out_of_range(token);
    }
    token = *(__shedskin__::str **)(__shedskin__::__char_cache + 8LL * *(unsigned __int8 *)(v3->qword10 + i_3));
    if ( *((_QWORD *)token + 3) != 1LL )
      __keygen__::validate_purplesyringa_key();
    if ( *(unsigned __int8 *)__shedskin__::str::c_str(token) != v26 )
      return (unsigned __int8)__shedskin__::False;
    if ( ++i_3 == 16 )
      return (unsigned __int8)__shedskin__::True;
    end1 = purplesyringa_key->end;
    start = purplesyringa_key->start;
  }
}
```

Можно упростить его дальше, заметив, что `__throw_index_out_of_range` принимает какой-то странный аргумент, не похожий ни на индекс, ни на тип какого-то значения; по-видимому, IDA опять неправильно вывела типы. Уберем аргумент из сигнатуры `__throw_index_out_of_range` и посмотрим, станет ли код проще:

```c
__int64 __fastcall __keygen__::validate_purplesyringa_key(__shedskin__::str *token, list_int *purplesyringa_key)
{
  __int64 i_1; // r12
  int *start1; // rcx
  int *end1; // rsi
  int *start; // rdx
  int *v8; // rax
  int v9; // r13d
  __int64 offset; // r14
  __int64 i; // r13
  __int64 v12; // r14
  int v13; // r12d
  int v14; // r12d
  int length; // ecx
  int v16; // r15d
  int j; // r14d
  signed int x_1; // eax
  signed int v19; // r12d
  int i_2; // r13d
  __int64 j_1; // r12
  int length_1; // ecx
  __int64 i_3; // r14
  __shedskin__::str *v24; // rdi
  int v25; // r15d
  __int64 (__fastcall *length_getter)(__shedskin__::str *__hidden); // rax

  i_1 = 0LL;
  start1 = purplesyringa_key->start;
  end1 = purplesyringa_key->end;
  start = start1;
  do
  {
    offset = i_1;
    if ( (int)i_1 >= (int)(end1 - start1) )
      __shedskin__::__throw_index_out_of_range();
    v8 = &start1[offset];
    v9 = start1[i_1];
    if ( !v9 )
    {
      v9 = 256;
      start = start1;
      v8 = &start1[offset];
    }
    ++i_1;
    *v8 = v9;
  }
  while ( i_1 != 16 );
  for ( i = 0LL; i != 15; ++i )
  {
    length = end1 - start;
    if ( length <= (int)i + 1 )
      __shedskin__::__throw_index_out_of_range();
    v12 = i;
    if ( length <= (int)i )
      __shedskin__::__throw_index_out_of_range();
    v13 = start[i] * start[i + 1] % 257;
    v14 = v13 + (v13 < 0 ? 257 : 0);
    if ( (int)i + 1 >= length )
      __shedskin__::__throw_index_out_of_range();
    start[v12 + 1] = v14;
  }
  v16 = 433;
  for ( j = 743893; j != 743893000; j += 743893 )
  {
    i_2 = (j >> 16) & 0xF;
    j_1 = (v16 >> 4) & 0xF;
    if ( i_2 != (_DWORD)j_1 )
    {
      length_1 = end1 - start;
      if ( i_2 >= length_1 )
        __shedskin__::__throw_index_out_of_range();
      if ( (int)j_1 >= length_1 )
        __shedskin__::__throw_index_out_of_range();
      x_1 = (unsigned __int8)(((unsigned int)((start[j_1] + start[i_2]) >> 31) >> 24) + LOBYTE(start[j_1]) + start[i_2])
          - ((unsigned int)((start[j_1] + start[i_2]) >> 31) >> 24);
      v19 = x_1 + 256;
      if ( x_1 >= 0 )
        v19 = x_1;
      if ( i_2 >= length_1 )
        __shedskin__::__throw_index_out_of_range();
      start[i_2] = v19;
    }
    v16 += 433;
  }
  i_3 = 0LL;
  while ( 1 )
  {
    if ( (int)i_3 >= (int)(end1 - start) )
      __shedskin__::__throw_index_out_of_range();
    v25 = start[i_3];
    length_getter = *(__int64 (__fastcall **)(__shedskin__::str *__hidden))(*(_QWORD *)token + 96LL);
    if ( length_getter == __shedskin__::str::__len__ )
    {
      if ( (int)i_3 >= *((_DWORD *)token + 6) )
        goto LABEL_36;
    }
    else if ( (int)i_3 >= (int)length_getter(token) )
    {
LABEL_36:
      __shedskin__::__throw_index_out_of_range();
    }
    v24 = *(__shedskin__::str **)(__shedskin__::__char_cache + 8LL * *(unsigned __int8 *)(*((_QWORD *)token + 2) + i_3));
    if ( *((_QWORD *)v24 + 3) != 1LL )
      __keygen__::validate_purplesyringa_key();
    if ( *(unsigned __int8 *)__shedskin__::str::c_str(v24) != v25 )
      return (unsigned __int8)__shedskin__::False;
    if ( ++i_3 == 16 )
      return (unsigned __int8)__shedskin__::True;
    end1 = purplesyringa_key->end;
    start = purplesyringa_key->start;
  }
}
```

Действительно, стало покороче. Теперь посмотрим на код сверху вниз по частям.

---

```c
i_1 = 0LL;
start1 = purplesyringa_key->start;
end1 = purplesyringa_key->end;
start = start1;
do
{
  offset = i_1;
  if ( (int)i_1 >= (int)(end1 - start1) )
    __shedskin__::__throw_index_out_of_range();
  v8 = &start1[offset];
  v9 = start1[i_1];
  if ( !v9 )
  {
    v9 = 256;
    start = start1;
    v8 = &start1[offset];
  }
  ++i_1;
  *v8 = v9;
}
while ( i_1 != 16 );
```

На Python это можно переписать как:

```python
for i_1 in range(16):
    v9 = purplesyringa_key[i_1]
    if not v9:
        v9 = 256
    purplesyringa_key[i_1] = v9
```

Таким образом, в ключе все значения `0` заменяются на `256`.

---

```c
for ( i = 0LL; i != 15; ++i )
{
  length = end1 - start;
  if ( length <= (int)i + 1 )
    __shedskin__::__throw_index_out_of_range();
  v12 = i;
  if ( length <= (int)i )
    __shedskin__::__throw_index_out_of_range();
  v13 = start[i] * start[i + 1] % 257;
  v14 = v13 + (v13 < 0 ? 257 : 0);
  if ( (int)i + 1 >= length )
    __shedskin__::__throw_index_out_of_range();
  start[v12 + 1] = v14;
}
```

На Python это можно переписать как:

```python
for i in range(15):
    v14 = purplesyringa_key[i] * purplesyringa_key[i + 1] % 257
    purplesyringa_key[i + 1] = v14
```

Таким образом, каждый элемент слева направо домножается на предыдущий по модулю 257.

---

```c
v16 = 433;
for ( j = 743893; j != 743893000; j += 743893 )
{
  i_2 = (j >> 16) & 0xF;
  j_1 = (v16 >> 4) & 0xF;
  if ( i_2 != (_DWORD)j_1 )
  {
    length_1 = end1 - start;
    if ( i_2 >= length_1 )
      __shedskin__::__throw_index_out_of_range();
    if ( (int)j_1 >= length_1 )
      __shedskin__::__throw_index_out_of_range();
    x_1 = (unsigned __int8)(((unsigned int)((start[j_1] + start[i_2]) >> 31) >> 24) + LOBYTE(start[j_1]) + start[i_2])
        - ((unsigned int)((start[j_1] + start[i_2]) >> 31) >> 24);
    v19 = x_1 + 256;
    if ( x_1 >= 0 )
      v19 = x_1;
    if ( i_2 >= length_1 )
      __shedskin__::__throw_index_out_of_range();
    start[i_2] = v19;
  }
  v16 += 433;
}
```

На Python это можно переписать как:

```python
v16 = 433
for j in range(743893, 743893000, 743893):
    i_2 = (j >> 16) & 0xf
    j_1 = (v16 >> 4) & 0xf
    if i_2 != j_1:
        x_1 = (unsigned __int8)(((unsigned int)((purplesyringa_key[j_1] + purplesyringa_key[i_2]) >> 31) >> 24) + LOBYTE(purplesyringa_key[j_1]) + purplesyringa_key[i_2]) - ((unsigned int)((purplesyringa_key[j_1] + purplesyringa_key[i_2]) >> 31) >> 24)  # ???
        v19 = x_1 + 256
        if x_1 >= 0:
            v19 = x_1
        purplesyringa_key[i_2] = v19
    v16 += 433
```

Правда, тут не особо понятно, что делает строка с `x_1 = ...`. Обозначим `a = purplesyringa_key[j_1]`, `b = purplesyringa_key[i_2]` и перепишем эту строчку как:

```c
x_1 = (unsigned __int8)(((unsigned int)((a + b) >> 31) >> 24) + LOBYTE(a) + b) - ((unsigned int)((a + b) >> 31) >> 24)  // ???
```

После предыдущего шага с взятием по модулю все значения в массиве точно между 0 и 256. Значит, `(a + b) >> 31` — это всегда 0. Скорректируем с учетом этого формулу и получим просто:

```c
x_1 = (__int8)(a + b)
```

С учетом этого код значительно упростится:

```python
v16 = 433
for j in range(743893, 743893000, 743893):
    i_2 = (j >> 16) & 0xf
    j_1 = (v16 >> 4) & 0xf
    if i_2 != j_1:
        purplesyringa_key[i_2] = (purplesyringa_key[j_1] + purplesyringa_key[i_2]) % 256
    v16 += 433
```

Можно пойти дальше и еще чуть его переписать, заметив, что `v16` и `j` — вообще говоря, равнозначные переменные, поскольку обе на каждой итерации инкрементируются на фиксированный шаг:

```python
for j in range(1, 1000):
    i_2 = ((j * 743893) >> 16) & 0xf
    j_1 = ((j * 433) >> 4) & 0xf
    if i_2 != j_1:
        purplesyringa_key[i_2] = (purplesyringa_key[j_1] + purplesyringa_key[i_2]) % 256
```

---

```c
i_3 = 0LL;
while ( 1 )
{
  if ( (int)i_3 >= (int)(end1 - start) )
    __shedskin__::__throw_index_out_of_range();
  v25 = start[i_3];
  length_getter = *(__int64 (__fastcall **)(__shedskin__::str *__hidden))(*(_QWORD *)token + 96LL);
  if ( length_getter == __shedskin__::str::__len__ )
  {
    if ( (int)i_3 >= *((_DWORD *)token + 6) )
      goto LABEL_36;
  }
  else if ( (int)i_3 >= (int)length_getter(token) )
  {
LABEL_36:
    __shedskin__::__throw_index_out_of_range();
  }
  v24 = *(__shedskin__::str **)(__shedskin__::__char_cache + 8LL * *(unsigned __int8 *)(*((_QWORD *)token + 2) + i_3));
  if ( *((_QWORD *)v24 + 3) != 1LL )
    __keygen__::validate_purplesyringa_key();
  if ( *(unsigned __int8 *)__shedskin__::str::c_str(v24) != v25 )
    return (unsigned __int8)__shedskin__::False;
  if ( ++i_3 == 16 )
    return (unsigned __int8)__shedskin__::True;
  end1 = purplesyringa_key->end;
  start = purplesyringa_key->start;
}
```

Эта часть читается хуже всего, поскольку здесь мы впервые сталкиваемся со строкой `token`. Попробуем сделать из `token` структуру и назвать в ней поля по аналогии с `list`:

```c
i_3 = 0LL;
while ( 1 )
{
  if ( (int)i_3 >= (int)(end1 - start) )
    __shedskin__::__throw_index_out_of_range();
  v25 = start[i_3];
  length_getter = *(__int64 (__fastcall **)(__shedskin__::str *__hidden))(token->object + 96LL);
  if ( length_getter == __shedskin__::str::__len__ )
  {
    if ( (int)i_3 >= token->length )
      goto LABEL_36;
  }
  else if ( (int)i_3 >= (int)length_getter((__shedskin__::str *)token) )
  {
LABEL_36:
    __shedskin__::__throw_index_out_of_range();
  }
  v24 = *(__shedskin__::str **)(__shedskin__::__char_cache + 8LL * (unsigned __int8)token->start[i_3]);
  if ( *((_QWORD *)v24 + 3) != 1LL )
    __keygen__::validate_purplesyringa_key();
  if ( *(unsigned __int8 *)__shedskin__::str::c_str(v24) != v25 )
    return (unsigned __int8)__shedskin__::False;
  if ( ++i_3 == 16 )
    return (unsigned __int8)__shedskin__::True;
  end1 = purplesyringa_key->end;
  start = purplesyringa_key->start;
}
```

Стало капельку получше. Видим цикл с 16 итерациями, на каждой из которых вычитывается очередной элемент из `purplesyringa_key` в `v25`, и из `token` в, по-видимому, `v24`.

`__char_cache` намекает на то, что Shed Skin компилирует обращение к индексу строки, которое в Python также возвращает строку длины 1, в получение строки из заранее подготовленной таблицы по индексу символа. Проверка с `!= 1LL` — по-видимому, проверка длины этой закешированной строки. Мы ожидаем, что длина всегда равна `1`, поэтому опустим это условие. `*c_str(v24)` вычитывает из строки первый символ — как раз `token[i_3]` — и сравнивает его с `v25`, то есть `purplesyringa_key[i_3]`. При несовпадении на какой-либо из итераций выдается `False`. Таким образом, код можно переписать на Python как:

```python
for i_3 in range(16):
    if purplesyringa_key[i] != ord(token[i]):
        return False
return True
```

---

Соберем все воедино и капельку причешем:

```python
# (1)
for i in range(16):
    purplesyringa_key[i] = purplesyringa_key[i] or 256

# (2)
for i in range(1, 16):
    purplesyringa_key[i] = purplesyringa_key[i] * purplesyringa_key[i - 1] % 257

# (3)
for i in range(1, 1000):
    a = ((i * 743893) >> 16) & 0xf
    b = ((i * 433) >> 4) & 0xf
    if a != b:
        purplesyringa_key[a] = (purplesyringa_key[a] + purplesyringa_key[b]) % 256

# (4)
return all(purplesyringa_key[i] == ord(token[i]) for i in range(16))
```

Теперь можно приступить к написанию кейгена для кейгена. Нужно подобрать такую бинарную строку `purplesyringa_key` длины 16, чтобы проверка (4) прошла.

---

После шага (3) `purplesyringa_key` должен совпадать с токеном. Посмотрим, возможно ли обратить действия шага (3), чтобы понять, чему `purplesyringa_key` должен был быть равен перед этим шагом.

На последней итерации при `i == 999` происходит следующее:

```python
i = 999
a = ((i * 743893) >> 16) & 0xf
b = ((i * 433) >> 4) & 0xf
if a != b:
    purplesyringa_key[a] = (purplesyringa_key[a] + purplesyringa_key[b]) % 256
```

`a` и `b` на этом шаге нам известны и их можно посчитать. Если они равны, то ничего обращать и не нужно; если равны, то чтобы обратить действие

```python
purplesyringa_key[a] = (purplesyringa_key[a] + purplesyringa_key[b]) % 256
```

нужно сделать

```python
purplesyringa_key[a] = (purplesyringa_key[a] - purplesyringa_key[b]) % 256
```

— прямо как если бы взятия по модулю не было. Это известное свойство арифметики по модулю.

После этого нужно обратить 998-ю итерацию, 997-ю и так далее — тем же методом. Запишем это кодом:

```python
for i in range(999, 0, -1):
    a = ((i * 743893) >> 16) & 0xf
    b = ((i * 433) >> 4) & 0xf
    if a != b:
        purplesyringa_key[a] = (purplesyringa_key[a] - purplesyringa_key[b]) % 256
```

После запуска этого куска мы узнаем, чему должен был быть равен `purplesyringa_key` перед шагом (3).

---

На шаге (2) происходит следующее:

```python
for i in range(1, 16):
    purplesyringa_key[i] = purplesyringa_key[i] * purplesyringa_key[i - 1] % 257
```

Для удобства анализа глазами раскроем цикл:

```python
purplesyringa_key[1 ] = purplesyringa_key[1 ] * purplesyringa_key[0 ] % 257
purplesyringa_key[2 ] = purplesyringa_key[2 ] * purplesyringa_key[1 ] % 257
purplesyringa_key[3 ] = purplesyringa_key[3 ] * purplesyringa_key[2 ] % 257
purplesyringa_key[4 ] = purplesyringa_key[4 ] * purplesyringa_key[3 ] % 257
purplesyringa_key[5 ] = purplesyringa_key[5 ] * purplesyringa_key[4 ] % 257
purplesyringa_key[6 ] = purplesyringa_key[6 ] * purplesyringa_key[5 ] % 257
purplesyringa_key[7 ] = purplesyringa_key[7 ] * purplesyringa_key[6 ] % 257
purplesyringa_key[8 ] = purplesyringa_key[8 ] * purplesyringa_key[7 ] % 257
purplesyringa_key[9 ] = purplesyringa_key[9 ] * purplesyringa_key[8 ] % 257
purplesyringa_key[10] = purplesyringa_key[10] * purplesyringa_key[9 ] % 257
purplesyringa_key[11] = purplesyringa_key[11] * purplesyringa_key[10] % 257
purplesyringa_key[12] = purplesyringa_key[12] * purplesyringa_key[11] % 257
purplesyringa_key[13] = purplesyringa_key[13] * purplesyringa_key[12] % 257
purplesyringa_key[14] = purplesyringa_key[14] * purplesyringa_key[13] % 257
purplesyringa_key[15] = purplesyringa_key[15] * purplesyringa_key[14] % 257
```

Чтобы обратить последнее действие, нужно, зная `a` и `c`, узнать такое `b`, что `a == b * c % 257`. Если бы взятия по модулю не было, мы бы сказали, что это просто деление: `b = a / c`. Но модуль тут есть, так что придется либо применить знания математики, либо погуглить и узнать, что [умножение по модулю тоже можно обращать](https://ru.wikipedia.org/wiki/%D0%9E%D0%B1%D1%80%D0%B0%D1%82%D0%BD%D0%BE%D0%B5_%D0%BF%D0%BE_%D0%BC%D0%BE%D0%B4%D1%83%D0%BB%D1%8E_%D1%87%D0%B8%D1%81%D0%BB%D0%BE). Более того, это действие [встроено](https://stackoverflow.com/a/9758173) в Python и может быть записано как:

```python
b = a * pow(c, -1, 257) % 257
```

Соответственно, обратить все 15 итераций можно так:

```python
for i in range(15, 0, -1):
    purplesyringa_key[i] = purplesyringa_key[i] * pow(purplesyringa_key[i - 1], -1, 257) % 257
```

Единственная проблема заключается в том, что... `purplesyringa_key[i - 1]` может быть нулём! А делить на ноль нельзя даже по модулю. Что же делать, если шаг (3) требует, чтобы какой-то элемент был равен `0`?

На самом деле, шаг (3) ничего такого не требует. Он может требовать, чтобы элемент был равен нулю *по модулю 256*. То есть он может спокойно быть равен −256, 0, 256, 512 и так далее. Получается, если нам кажется, что если какой-то элемент должен быть равен нулю, можно просто заменить этот нуль на 256, и шаг (3) продолжит работать успешно:

```python
for i in range(16):
    purplesyringa_key[i] = purplesyringa_key[i] or 256
for i in range(15, 0, -1):
    purplesyringa_key[i] = purplesyringa_key[i] * pow(purplesyringa_key[i - 1], -1, 257) % 257
```

Теперь проблем с делением на 0 быть не должно.

---

Наконец, нужно обратить первый шаг:

```python
for i in range(16):
    purplesyringa_key[i] = purplesyringa_key[i] or 256
```

Здесь все просто. Можно оставить все элементы как есть. Но если какой-то элемент после шага (1) должен быть равен `256`, можно его заменить на `0` (оставить его как есть со значением 256 нельзя, потому что байт не может быть равен числу 256, а вот нулю вполне может).

Таким образом, обращение этого шага можно записать так:

```python
for i in range(16):
    purplesyringa_key[i] = purplesyringa_key[i] % 256
```

Отметим, кстати, одну неочевидную деталь. На прошлом шаге (2) мы в частности заменяли последний элемент массива на 256, если он был равен 0. При этом формально шаг (2) такой замены не требует, ведь на последний элемент массива мы никогда не делим. Однако, если бы мы не произвели эту замену, могло бы оказаться так, что перед шагом (2) должно выполняться `purplesyringa_key[15] == 0`, но после шага (1) элемент никогда не может быть равен нулю!

---

Объединим куски кейгена для кейгена воедино и добавим ввод-вывод:

```python
token = input("Token: ")
assert len(token) == 16
purplesyringa_key = list(token.encode())

for i in range(999, 0, -1):
    a = ((i * 743893) >> 16) & 0xf
    b = ((i * 433) >> 4) & 0xf
    if a != b:
        purplesyringa_key[a] = (purplesyringa_key[a] - purplesyringa_key[b]) % 256

for i in range(15, 0, -1):
    purplesyringa_key[i] = purplesyringa_key[i] * pow(purplesyringa_key[i - 1] or 256, -1, 257) % 257

for i in range(16):
    purplesyringa_key[i] = purplesyringa_key[i] % 256

print(bytes(purplesyringa_key).hex())
```

Запустим:

```
Token: maziserywq8vln9u
f3282ca56dd4d755d65731a947cec876
```

Теперь подставим этот ключ в кейген:

```
UCUCUGA PRO KEYGEN by xXx_HACKERNAME_xXx
Enter token: maziserywq8vln9u
You need to obtain a key from me to use this keygen.
Please mail purplesyringa@example.com. We will agree on the payment.
Enter key from purplesyringa: f3282ca56dd4d755d65731a947cec876
UCUCUGA Pro key: egDNw8_x1gQtDy8_
```

Наконец можно скачать уцуцугу!

Флаг: **ugra_was_is_worth_it_ff6x8jwrzr6t**
