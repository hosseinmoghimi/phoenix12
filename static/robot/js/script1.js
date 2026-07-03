    document.addEventListener("DOMContentLoaded", function () {
            const cards = document.querySelectorAll(
              ".more-templates-badge-wrapper",
            );
            let currentIndex = 0;
            const ANIMATION_INTERVAL = 8000; // 8 seconds

            function updateCards() {
              cards.forEach((card, index) => {
                card.classList.remove("active", "next");

                if (index === currentIndex) {
                  card.classList.add("active");
                } else if (index === (currentIndex + 1) % cards.length) {
                  card.classList.add("next");
                }
              });

              currentIndex = (currentIndex + 1) % cards.length;
            }

            // Initial state
            updateCards();

            // Start the loop
            setInterval(updateCards, ANIMATION_INTERVAL);
          });
       