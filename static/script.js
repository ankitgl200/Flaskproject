document.addEventListener("DOMContentLoaded", () => {
    const navToggle = document.getElementById("navToggle");
    const navLinks = document.getElementById("navLinks");

    if (navToggle && navLinks) {
        navToggle.addEventListener("click", () => {
            navLinks.classList.toggle("show");
        });
    }

    const yearSpan = document.getElementById("year");
    if (yearSpan) {
        yearSpan.textContent = new Date().getFullYear();
    }
});


// filter
document.addEventListener("DOMContentLoaded", () => {

    const filterButtons = document.querySelectorAll(".filter-btn");
    const cards = document.querySelectorAll(".note-card");

    filterButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const filter = btn.dataset.filter;

            // update active button
            filterButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            cards.forEach(card => {
                const subject = card.dataset.subject;

                if (filter === "all" || filter === subject) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });

});

function login(){
    window.location.href= "login"
}

function showmore() {
    const showDiv = document.getElementById("show");
    if (showDiv.style.display === "none") {
        showDiv.style.display = "flex";
    } else {
        showDiv.style.display = "none";
    }
}