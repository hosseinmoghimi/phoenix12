
gsap.registerPlugin(ScrollTrigger, Observer);

      document.addEventListener("DOMContentLoaded", function () {
        initMarqueeAnimation();
        initCounterAnimation();
      });

      // ============================================
      // MARQUEE SCROLL ANIMATION
      // ============================================
      function initMarqueeAnimation() {
        const marqueeObject = { value: 1 };
        const marqueeObjectInverse = { value: 1 }; // Initial value should be positive for L-R movement

        // Create marquee timeline with GSAP for regular items
        const marqueeTimeline = gsap.timeline({
          repeat: -1,
          onReverseComplete: () => {
            marqueeTimeline.progress(1);
          },
        });

        // Set up marquee animation for regular items (0% to -100%)
        marqueeTimeline.fromTo(
          ".marquee-scroll-item",
          { xPercent: 0 },
          {
            xPercent: -100,
            duration: 50, // Adjust for marquee speed
            ease: "none",
          },
        );

        // Create marquee timeline with GSAP for inverse items
        const marqueeTimelineInverse = gsap.timeline({
          repeat: -1,
          onReverseComplete: () => {
            marqueeTimelineInverse.progress(1);
          },
        });

        // Set up marquee animation for inverse items (-100% to 0%)
        marqueeTimelineInverse.fromTo(
          ".marquee-scroll-item-inverse",
          { xPercent: -100 },
          {
            xPercent: 0,
            duration: 50, // Adjust for marquee speed
            ease: "none",
          },
        );

        // Create Observer for scroll interaction
        Observer.create({
          target: window,
          type: "wheel,scroll,touch",
          onChangeY: (self) => {
            let velocity = self.velocityY * 0.002;
            velocity = gsap.utils.clamp(-40, 40, velocity);

            // Apply velocity to regular marquee
            marqueeTimeline.timeScale(velocity);

            // Determine the target resting speed for regular marquee
            let restingSpeed = velocity < 0 ? -1 : 1;

            // Determine the target resting speed for inverse marquee
            // If scrolling down (positive velocity), inverse should move L-R (positive timeScale)
            // If scrolling up (negative velocity), inverse should move R-L (negative timeScale)
            let restingSpeedInverse = velocity < 0 ? -1 : 1;

            // Animate timeScale change for regular marquee
            gsap.fromTo(
              marqueeObject,
              { value: velocity },
              {
                value: restingSpeed,
                duration: 1,
                onUpdate: () => {
                  marqueeTimeline.timeScale(marqueeObject.value);
                },
              },
            );

            // Animate timeScale change for inverse marquee
            gsap.fromTo(
              marqueeObjectInverse,
              { value: velocity }, // Start with the same velocity value
              {
                value: restingSpeedInverse, // Target the inverse resting speed
                duration: 1,
                onUpdate: () => {
                  marqueeTimelineInverse.timeScale(marqueeObjectInverse.value);
                },
              },
            );
          },
        });

        // Handle reduced motion preference
        const reduceMotion = window.matchMedia(
          "(prefers-reduced-motion: reduce)",
        );
        if (reduceMotion.matches) {
          marqueeTimeline.pause();
          marqueeTimelineInverse.pause(); // Pause inverse marquee as well
        }
      }

      // ============================================
      // NUMBER COUNTER ANIMATION
      // ============================================
      function initCounterAnimation() {
        function numberWithCommas(x, decimals = 0) {
          return x.toLocaleString(undefined, {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals,
          });
        }

        const counterElements = gsap.utils.toArray(
          ".count-up-number-animation",
        );
        if (!counterElements.length) return;

        counterElements.forEach((element, index) => {
          const targetValue =
            parseFloat(element.getAttribute("data-count")) || 100;
          const decimals = targetValue % 1 !== 0 ? 1 : 0;

          // Create counter animation with GSAP
          gsap.fromTo(
            element,
            { textContent: 0 },
            {
              textContent: targetValue,
              duration: 2,
              ease: "power1.out",
              snap: decimals ? { textContent: 0.1 } : { textContent: 1 },
              delay: index * 0.1,
              scrollTrigger: {
                trigger: element,
                start: "top 80%",
                once: true,
                toggleActions: "play none none none",
              },
              onUpdate: function () {
                const currentValue = parseFloat(element.textContent);
                element.textContent = numberWithCommas(currentValue, decimals);
              },
            },
          );
        });

        window.addEventListener("load", () => {
          ScrollTrigger.refresh();
        });
      }

      // ============================================
      // ADDITIONAL GSAP UTILITIES
      // ============================================
      ScrollTrigger.batch(".animate-on-scroll", {
        onEnter: (batch) =>
          gsap.to(batch, { opacity: 1, y: 0, stagger: 0.15, overwrite: true }),
        onLeave: (batch) =>
          gsap.set(batch, { opacity: 0, y: 100, overwrite: true }),
        onEnterBack: (batch) =>
          gsap.to(batch, { opacity: 1, y: 0, stagger: 0.15, overwrite: true }),
        onLeaveBack: (batch) =>
          gsap.set(batch, { opacity: 0, y: -100, overwrite: true }),
      });