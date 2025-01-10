import { Card } from '../../../components/ui/Card';
import { testExpectations } from '../../../data/guides/testExpectations';

export function TestExpectations() {
  return (
    <>
      <Card.Header className="border-b border-gray-200 bg-gray-50">
        <Card.Title className="text-2xl">{testExpectations.title}</Card.Title>
        <p className="mt-2 text-gray-600">Duration: {testExpectations.duration}</p>
      </Card.Header>

      <Card.Content className="divide-y divide-gray-200">
        {testExpectations.sections.map((section) => (
          <div key={section.title} className="py-6 first:pt-0 last:pb-0">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              {section.title}
            </h3>
            <ul className="space-y-3">
              {section.content.map((item) => (
                <li key={item} className="flex items-start">
                  <span className="flex-shrink-0 h-5 w-5 text-indigo-600">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M16.704 4.153a.75.75 0 01.143 1.052l-8 10.5a.75.75 0 01-1.127.075l-4.5-4.5a.75.75 0 011.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 011.05-.143z" clipRule="evenodd" />
                    </svg>
                  </span>
                  <span className="ml-3 text-gray-600">{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </Card.Content>
    </>
  );
}