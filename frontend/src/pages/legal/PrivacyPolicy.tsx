import { useEffect } from 'react';
import { Helmet } from 'react-helmet-async';

export default function PrivacyPolicy() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const lastUpdated = new Date().toLocaleDateString('en-CA');

  return (
    <>
      <Helmet>
        <title>Privacy Policy - ICBC Road Test Notifier</title>
        <meta name="description" content="Privacy Policy for ICBC Road Test Notifier" />
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Privacy Policy",
            "dateModified": lastUpdated
          })}
        </script>
      </Helmet>

      <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <article className="prose prose-indigo max-w-none">
          <h1>Privacy Policy</h1>
          <p className="text-sm text-gray-500">Last Updated: {lastUpdated}</p>

          <section>
            <h2>PIPEDA and BC PIPA Compliance Statement</h2>
            <p>ICBC Road Test Notifier ("we", "our", or "us") is committed to protecting your privacy and complying with applicable data protection laws, including the Personal Information Protection and Electronic Documents Act (PIPEDA) and the British Columbia Personal Information Protection Act (BC PIPA).</p>
          </section>

          <section>
            <h2>Data Collection and Usage</h2>
            <p>We collect and use personal information for the following purposes:</p>
            <ul>
              <li>To provide road test notification services</li>
              <li>To process payments and manage subscriptions</li>
              <li>To communicate important service updates</li>
              <li>To improve our services and user experience</li>
            </ul>
          </section>

          <section>
            <h2>Data Storage and Security</h2>
            <p>All personal information is stored on secure servers located in Canada. We implement appropriate technical and organizational measures to protect your data.</p>
          </section>

          <section>
            <h2>Cookie Usage</h2>
            <h3>Essential Cookies</h3>
            <p>Required for basic website functionality and security.</p>
            
            <h3>Optional Cookies</h3>
            <p>Used for analytics and performance optimization. You can opt-out of these cookies.</p>
          </section>

          <section>
            <h2>Data Retention</h2>
            <p>We retain personal information for as long as necessary to provide our services and comply with legal obligations. Account information is retained for 24 months after account closure.</p>
          </section>

          <section>
            <h2>Your Rights</h2>
            <p>Under Canadian privacy laws, you have the right to:</p>
            <ul>
              <li>Access your personal information</li>
              <li>Correct inaccurate information</li>
              <li>Withdraw consent</li>
              <li>File a complaint</li>
            </ul>
          </section>

          <section>
            <h2>Contact Information</h2>
            <p>Privacy Officer: [Name]<br />
            Email: privacy@icbcnotifier.ca<br />
            Phone: [Phone Number]<br />
            Address: [Address], British Columbia, Canada</p>
          </section>

          <section>
            <h2>Updates to This Policy</h2>
            <p>We review and update this policy quarterly. Changes will be posted on this page with an updated revision date.</p>
          </section>
        </article>
      </div>
    </>
  );
}