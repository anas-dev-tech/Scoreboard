document.addEventListener("alpine:init", () => {
  // Alpine.data("dropdown", () => ({
  //   open: false,
  //   toggle() {
  //     this.open = !this.open;
  //   },
  // }));

  Alpine.store('currentUser', {
    name: 'John Doe',
    email: 'johndoe@example.com',
  });
});

Alpine.start()
