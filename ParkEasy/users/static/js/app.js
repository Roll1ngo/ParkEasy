 const numberPlates = [];
        const numberPlatesCount = 50; // Кількість табличок
        const plateWidth = 140; // Ширина таблички
        const plateHeight = 30; // Висота таблички
        const minSpacing = 20; // Мінімальна відстань між табличками

        // Генерація випадкових номерних табличок
        function generateRandomPlate() {
            const regions = ["AA", "AB", "AC", "AE", "AH", "AI", "AK", "AM", "AO", "AP", "AT", "AX", "BA", "BB", "BC", "BE", "BH", "BI", "BK", "BM", "BO", "BT", "BX", "CA", "CB", "CE", "CH", "CI", "CK", "CM", "CO", "CT", "CX"];
            const letters = "АВЕКМНОРСТУХ";
            const randomRegion = regions[Math.floor(Math.random() * regions.length)];
            const randomNumbers = Math.floor(1000 + Math.random() * 9000);
            const randomLetters = letters.charAt(Math.floor(Math.random() * letters.length)) + letters.charAt(Math.floor(Math.random() * letters.length));

            return `${randomRegion} ${randomNumbers} ${randomLetters}`;
        }

        // Перевірка на перекриття
        function isOverlapping(x, y) {
            return numberPlates.some(plate => {
                const plateRect = plate.getBoundingClientRect();
                return !(x > plateRect.right + minSpacing ||
                         x + plateWidth < plateRect.left - minSpacing ||
                         y > plateRect.bottom + minSpacing ||
                         y + plateHeight < plateRect.top - minSpacing);
            });
        }

        // Розміщення табличок
        function placePlates() {
            numberPlates.forEach(plate => {
                let x, y;
                do {
                    x = Math.random() * (window.innerWidth - plateWidth);
                    y = Math.random() * (window.innerHeight - plateHeight);
                } while (isOverlapping(x, y));

                plate.style.left = `${x}px`;
                plate.style.top = `${y}px`;
            });
        }

        // Створення елемента номерної таблички
        function createNumberPlate() {
            const plateText = generateRandomPlate();

            const plateElement = document.createElement("div");
            plateElement.className = "number-plate";

            const blueSection = document.createElement("div");
            blueSection.className = "blue-section";

            const flagElement = document.createElement("div");
            flagElement.className = "flag";

            const uaText = document.createElement("div");
            uaText.className = "ua-text";
            uaText.textContent = "UA";

            blueSection.appendChild(flagElement);
            blueSection.appendChild(uaText);

            plateElement.appendChild(blueSection);
            plateElement.appendChild(document.createTextNode(plateText));

            document.body.appendChild(plateElement);
            numberPlates.push(plateElement);
        }

        // Анімація дощу табличок
        function animatePlates() {
            numberPlates.forEach(plate => {
                let top = parseFloat(plate.style.top);
                top += 1; // Швидкість дощу
                if (top > window.innerHeight) top = -plateHeight; // Перезапуск з верху

                plate.style.top = top + 'px';
            });

            requestAnimationFrame(animatePlates);
        }

        for (let i = 0; i < numberPlatesCount; i++) {
            createNumberPlate();
        }

        placePlates();

        animatePlates();