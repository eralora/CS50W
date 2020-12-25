txt = document.querySelector("#add-text");
btn= document.querySelector("#add-btn");
btn.addEventListener("click", () => {
	text = txt.value;

	if (text.length != 0 ) {
		form = new FormData();
		form.append("post", text.trim());
		fetch("/addpost/", {
			method: "POST",
			body: form,

		})

		.then((res) => res.json())
		.then((res) => {
			if (res.status == 201) {
				add_html(
					res.post_id)
			}
		})
	}
})
