import { PageMetadata } from '../../components/common/PageMetadata';
import { metadata } from '../../config/metadata';
import { GuideSection } from './components/GuideSection';
import { TestExpectations } from './components/TestExpectations';
import { EssentialSkills } from './components/EssentialSkills';
import { RequiredDocuments } from './components/RequiredDocuments';

export default function RoadTestGuide() {
  return (
    <>
      <PageMetadata {...metadata.guides} />

      <div className="max-w-4xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 sm:text-5xl mb-4">
            BC Class 5 Road Test Guide
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Everything you need to know to prepare for your ICBC road test, from required documents to essential skills.
          </p>
        </header>

        <div className="space-y-16">
          <GuideSection>
            <TestExpectations />
          </GuideSection>

          <GuideSection>
            <EssentialSkills />
          </GuideSection>

          <GuideSection>
            <RequiredDocuments />
          </GuideSection>
        </div>
      </div>
    </>
  );
}