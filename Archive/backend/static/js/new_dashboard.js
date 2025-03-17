document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ New Dashboard Loaded!");

    function attachListeners() {
        console.log("🔄 Attaching event listeners to buttons...");
        document.querySelectorAll("button, .nav-btn").forEach(btn => {
            console.log(`🎯 Attaching to: ${btn.innerText}`);

            // Remove any existing event listeners to prevent duplicates
            btn.replaceWith(btn.cloneNode(true));
            
            btn.addEventListener("click", () => alert(`✅ Click detected: ${btn.innerText}`));
        });
    }

    attachListeners(); // Attach listeners when page loads

    // Fix navigation buttons
    document.getElementById("add-category-btn").addEventListener("click", function () {
        let category = prompt("Enter new category:");
        if (category) {
            fetch("/add_category", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ category })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                attachListeners(); // Ensure new buttons get listeners
            });
        }
    });

    document.getElementById("view-categories-btn").addEventListener("click", function () {
        fetch("/get_categories")
            .then(response => response.json())
            .then(data => {
                let categoryList = document.getElementById("category-list");
                categoryList.innerHTML = "";
                data.categories.forEach(cat => {
                    let listItem = document.createElement("li");
                    listItem.textContent = cat.category;
                    categoryList.appendChild(listItem);
                });
                document.getElementById("category-section").style.display = "block";

                attachListeners(); // Ensure buttons inside category section are active
            });
    });

    // Ensure event listeners reattach if needed
    setTimeout(attachListeners, 1500);
});
