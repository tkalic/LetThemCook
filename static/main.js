function showTab(index) {
    const tabs = document.querySelectorAll('.tab');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach((tab, i) => {
      tab.classList.toggle('active', i === index);
    });

    contents.forEach((content, i) => {
      content.classList.toggle('active', i === index);
    });
  }