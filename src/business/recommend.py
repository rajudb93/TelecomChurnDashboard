def recommend_action(prob, customer_name="Customer"):

    if prob > 0.7:
        subject = "We Value You – Exclusive Offer Just for You"

        message = f"""
Dear {customer_name},

We noticed that your recent experience may not have been up to the mark, and we truly value your relationship with us.

To ensure you continue enjoying our services, we’re offering you an exclusive discount along with priority customer support assistance.

Our team is ready to help you resolve any issues and enhance your experience.

👉 Special Benefits for You:
- Personalized support
- Exclusive discount on your plan
- Faster issue resolution

Please feel free to reach out to us anytime — we’re here to help.

Warm regards,  
Customer Success Team
"""

        action = "🔥 High Risk – Offer discount + priority support"

    elif prob > 0.4:
        subject = "We’re Here to Improve Your Experience"

        message = f"""
Dear {customer_name},

We hope you're doing well.

We wanted to check in and ensure that you’re getting the best value from our services. If there’s anything we can improve or assist you with, we’d love to hear from you.

👉 Here’s what we can help with:
- Optimizing your current plan
- Resolving any service issues
- Providing personalized recommendations

Your feedback matters to us, and we’re committed to making your experience better.

Looking forward to hearing from you.

Best regards,  
Customer Experience Team
"""

        action = "⚠️ Medium Risk – Engagement email"

    else:
        subject = "Unlock More Value with Our Premium Features"

        message = f"""
Dear {customer_name},

Thank you for being a valued customer!

We’re excited to offer you an opportunity to enhance your experience with our premium features designed to give you even more value.

👉 Upgrade Benefits:
- Enhanced service features
- Priority access to new updates
- Better performance and reliability

We believe this upgrade can help you get even more out of our services.

Let us know if you'd like to explore these options!

Best regards,  
Growth Team
"""

        action = "💎 Low Risk – Upsell opportunity"

    return {
        "action": action,
        "subject": subject,
        "message": message,
    }