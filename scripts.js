//Connexion
const signinForm = document.getElementById('signinForm');
if (signinForm) {
    signinForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const emailOrPhone = document.getElementById('emailOrPhone').value;
        const password = document.getElementById('password').value;
        
        // Basic validation
        if (emailOrPhone && password) {
            // Get stored user data from localStorage
            const user = JSON.parse(localStorage.getItem('user')) || {};
            
            // Check if login with email or phone number
            if ((user.email === emailOrPhone || user.number === emailOrPhone) && user.password === password) {
                alert('Connexion réussie!');
                // Redirect to dashboard or home page
                window.location.href = 'index.html';
            } else {
                alert('Adresse mail/numéro de téléphone ou mot de passe invalide.');
            }
        }
    });
}

// Inscription  
const signupForm = document.getElementById('signupForm');
if (signupForm) {
    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const email = document.getElementById('email').value;
        const number = document.getElementById('number').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Validation
        if (!username || !email || !number || !password || !confirmPassword) {
            alert('Veuillez remplir tous les champs.');
            return;
        }
        
        if (password !== confirmPassword) {
            alert('Les mots de passe ne correspondent pas.');
            return;
        }
        
        if (password.length < 6) {
            alert('Votre mot de passe doit contenir au moins 6 caractères.');
            return;
        }
        
        // Email validation
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            alert('Veuillez entrer une adresse mail valide.');
            return;
        }
        
        // Check if account already exists
        const existingUser = JSON.parse(localStorage.getItem('user')) || {};
        if (existingUser.email === email || existingUser.number === number || existingUser.username === username) {
            alert('Un compte avec cet identifiant, email ou numéro de téléphone existe déjà. Veuillez vous connecter ou utiliser d\'autres informations.');
            return;
        }
        
        // Store user data in localStorage 
        const user = {
            username: username,
            email: email,
            number: number,
            password: password
        };
        
        localStorage.setItem('user', JSON.stringify(user));
        alert('Votre compte a été créé avec succès ! Vous pouvez maintenant vous connecter.');
        window.location.href = 'signin.html';
    });
}
