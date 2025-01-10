import { useEffect } from 'react';
import { Helmet } from 'react-helmet-async';

export default function Terms() {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  const lastUpdated = new Date().toLocaleDateString('en-CA');

  return (
    <>
      <Helmet>
        <title>Terms and Conditions - ICBC Road Test Notifier</title>
        <meta name="description" content="Terms and Conditions for ICBC Road Test Notifier" />
        <script type="application/ld+json">
          {JSON.stringify({
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": "Terms and Conditions",
            "dateModified": lastUpdated
          })}
        </script>
      </Helmet>

      <div className="max-w-4xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <article className="prose prose-indigo max-w-none">
          <h1>Terms and Conditions</h1>
          <p className="text-sm text-gray-500">Last Updated: {lastUpdated}</p>

          <section>
            <h2>1. Jurisdiction</h2>
            <p>These terms are governed by the laws of British Columbia, Canada. Any disputes shall be resolved exclusively in the courts of British Columbia.</p>
          </section>

          <section>
            <h2>2. Service Availability</h2>
            <p>Our services are primarily intended for users in British Columbia, Canada. While we accept international users, service availability and features may vary by region.</p>
          </section>

          <section>
            <h2>3. Pricing and Taxes</h2>
            <p>All prices are in Canadian dollars (CAD). GST (5%) and PST (7%) will be applied to all purchases as required by BC law.</p>
          </section>

          <section>
            <h2>4. Consumer Protection</h2>
            <p>Our services comply with the BC Consumer Protection Act. You have certain rights under this law, including the right to cancel services within specified timeframes.</p>
          </section>

          <section>
            <h2>5. Anti-Spam Compliance</h2>
            <p>We comply with Canada's Anti-Spam Legislation (CASL). You may withdraw consent to receive commercial electronic messages at any time.</p>
          </section>

          <section>
            <h2>6. Dispute Resolution</h2>
            <p>Disputes may be resolved through:</p>
            <ol>
              <li>Direct negotiation</li>
              <li>Mediation</li>
              <li>BC Small Claims Court (for claims up to $35,000)</li>
            </ol>
          </section>

          <section>
            <h2>7. Severability</h2>
            <p>If any provision of these terms is found to be unenforceable, the remaining provisions will continue in full force and effect.</p>
          </section>

          <section>
            <h2>8. Business Information</h2>
            <p>ICBC Road Test Notifier<br />
            BC Business Registration: [Number]<br />
            Address: [Address]<br />
            Email: legal@icbcnotifier.ca<br />
            Phone: [Phone Number]</p>
          </section>

          <section>
            <h2>9. Amendments</h2>
            <p>We reserve the right to modify these terms at any time. Changes will be effective immediately upon posting to our website. Continued use of our services constitutes acceptance of modified terms.</p>
          </section>
        </article>
      </div>
    </>
  );
}