// Customer Churn Prediction - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    const resultsContainer = document.getElementById('results');

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Show loading state
        setLoading(true);
        
        try {
            const formData = new FormData(form);
            
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('Failed to connect to the server. Please try again.');
        } finally {
            setLoading(false);
        }
    });

    // Auto-calculate total charges based on tenure and monthly charges
    const tenureInput = document.getElementById('tenure');
    const monthlyChargesInput = document.getElementById('MonthlyCharges');
    const totalChargesInput = document.getElementById('TotalCharges');

    function updateTotalCharges() {
        const tenure = parseFloat(tenureInput.value) || 0;
        const monthlyCharges = parseFloat(monthlyChargesInput.value) || 0;
        const estimated = tenure * monthlyCharges;
        totalChargesInput.value = estimated.toFixed(2);
    }

    tenureInput.addEventListener('input', updateTotalCharges);
    monthlyChargesInput.addEventListener('input', updateTotalCharges);

    // Set loading state
    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        btnText.style.display = isLoading ? 'none' : 'inline';
        btnLoader.style.display = isLoading ? 'inline-flex' : 'none';
    }

    // Display prediction results
    function displayResults(data) {
        resultsContainer.style.display = 'block';
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
        // Update prediction result
        const predictionResult = document.getElementById('prediction-result');
        const resultIcon = document.getElementById('result-icon');
        
        if (data.prediction === 'Yes') {
            predictionResult.textContent = 'Will Churn';
            predictionResult.className = 'result-value churn';
            resultIcon.innerHTML = '⚠️';
            resultIcon.className = 'result-icon churn';
        } else {
            predictionResult.textContent = 'Will Stay';
            predictionResult.className = 'result-value no-churn';
            resultIcon.innerHTML = '✅';
            resultIcon.className = 'result-icon no-churn';
        }
        
        // Update probability bars with animation
        const churnProb = document.getElementById('churn-prob');
        const churnBar = document.getElementById('churn-bar');
        const retainProb = document.getElementById('retain-prob');
        const retainBar = document.getElementById('retain-bar');
        
        // Reset bars first
        churnBar.style.width = '0%';
        retainBar.style.width = '0%';
        
        // Animate after a brief delay
        setTimeout(() => {
            churnProb.textContent = data.churn_probability + '%';
            churnBar.style.width = data.churn_probability + '%';
            
            retainProb.textContent = data.no_churn_probability + '%';
            retainBar.style.width = data.no_churn_probability + '%';
        }, 100);
        
        // Update risk badge
        const riskBadge = document.getElementById('risk-badge');
        riskBadge.textContent = data.risk_level + ' Risk';
        riskBadge.className = 'risk-badge ' + data.risk_level.toLowerCase();
    }

    // Show error message
    function showError(message) {
        // Create error toast if it doesn't exist
        let errorToast = document.querySelector('.error-toast');
        if (!errorToast) {
            errorToast = document.createElement('div');
            errorToast.className = 'error-toast';
            errorToast.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
                color: white;
                padding: 15px 25px;
                border-radius: 10px;
                font-weight: 500;
                box-shadow: 0 4px 20px rgba(235, 51, 73, 0.4);
                z-index: 1000;
                animation: slideInRight 0.3s ease;
            `;
            document.body.appendChild(errorToast);
        }
        
        errorToast.textContent = message;
        errorToast.style.display = 'block';
        
        // Add slide in animation
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideInRight {
                from {
                    opacity: 0;
                    transform: translateX(100px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
        `;
        document.head.appendChild(style);
        
        // Auto hide after 5 seconds
        setTimeout(() => {
            errorToast.style.display = 'none';
        }, 5000);
    }

    // Dynamic field updates based on internet service selection
    const internetServiceSelect = document.getElementById('InternetService');
    const internetDependentFields = [
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 
        'TechSupport', 'StreamingTV', 'StreamingMovies'
    ];

    internetServiceSelect.addEventListener('change', function() {
        const value = this.value;
        internetDependentFields.forEach(fieldId => {
            const select = document.getElementById(fieldId);
            if (value === 'No') {
                select.value = 'No internet service';
            }
        });
    });

    // Dynamic field updates based on phone service selection
    const phoneServiceSelect = document.getElementById('PhoneService');
    const multipleLinesSelect = document.getElementById('MultipleLines');

    phoneServiceSelect.addEventListener('change', function() {
        if (this.value === 'No') {
            multipleLinesSelect.value = 'No phone service';
        }
    });

    // Initial total charges calculation
    updateTotalCharges();
});
