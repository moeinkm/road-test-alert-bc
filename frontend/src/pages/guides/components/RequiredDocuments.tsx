import { Card } from '../../../components/ui/Card';
import { requiredDocuments } from '../../../data/guides/requiredDocuments';

export function RequiredDocuments() {
  return (
    <>
      <Card.Header className="border-b border-gray-200 bg-gray-50">
        <Card.Title className="text-2xl">{requiredDocuments.title}</Card.Title>
      </Card.Header>

      <Card.Content className="divide-y divide-gray-200">
        {requiredDocuments.sections.map((section) => (
          <div key={section.title} className="py-6 first:pt-0 last:pb-0">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {section.title}
            </h3>
            <div className="bg-white rounded-lg border border-gray-200 divide-y divide-gray-200">
              {section.items.map((item) => (
                <div key={item.name} className="p-4 flex items-start">
                  <div className="flex-shrink-0">
                    {item.required && (
                      <span className="inline-flex items-center rounded-full bg-red-100 px-2.5 py-0.5 text-xs font-medium text-red-700">
                        Required
                      </span>
                    )}
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium text-gray-900">{item.name}</p>
                    <p className="mt-1 text-sm text-gray-500">{item.description}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}

        <div className="py-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Payment Information
          </h3>
          <div className="bg-gray-50 rounded-lg p-4">
            <dl className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div>
                <dt className="text-sm font-medium text-gray-500">Payment Methods</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {requiredDocuments.paymentInfo.methods.join(', ')}
                </dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Amount</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {requiredDocuments.paymentInfo.amount}
                </dd>
              </div>
              <div className="sm:col-span-2">
                <dt className="text-sm font-medium text-gray-500">Refund Policy</dt>
                <dd className="mt-1 text-sm text-gray-900">
                  {requiredDocuments.paymentInfo.refundPolicy}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </Card.Content>
    </>
  );
}