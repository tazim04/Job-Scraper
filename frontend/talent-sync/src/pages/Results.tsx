import {
  Star,
  ClipboardList,
  Briefcase,
  MapPin,
  Clock,
  Zap,
  Lightbulb,
  ArrowLeft,
  CircleDollarSign,
} from "lucide-react";
import { ReactNode } from "react";
import { useNavigate } from "../hooks/useNavigate";
import NavigateOptions from "../types/navigation/NavigateOptions";

// Reusable Section Component
interface SectionProps {
  title: string;
  icon: ReactNode;
  children: ReactNode;
}

const Section = ({ title, icon, children }: SectionProps) => (
  <div className="bg-gray-50 p-4 rounded-lg">
    <div className="flex items-center gap-2 mb-3">
      <div className="text-indigo-500">{icon}</div>
      <h3 className="font-semibold text-gray-900">{title}</h3>
    </div>
    {children}
  </div>
);

// Main Results Component
const Results = () => {
  const { resultsData, clearResults, navigate } = useNavigate();
  const backPayload: NavigateOptions = {
    page: "dashboard",
    subPage: "scanner",
  };
  const handleBack = () => {
    clearResults(); // Clear results data
    navigate(backPayload); // Navigate back to scanner
  };

  if (resultsData?.error) {
    return (
      <div className="flex flex-col items-center justify-center text-center p-2">
        <h2 className="text-xl font-semibold text-red-600">
          WOAH! Something went wrong!
        </h2>
        <p className="text-gray-700 mt-2 text-base">{resultsData.reason}</p>
        <p className="mt-4">{resultsData.error}</p>
        <button
          onClick={handleBack}
          className="bg-indigo-500 text-white px-4 py-2 rounded mt-4 transition-colors ease-in-out hover:bg-indigo-400"
        >
          Back to Scanner
        </button>
      </div>
    );
  }

  if (!resultsData) {
    return <div>No results data available.</div>;
  }

  return (
    <div className="px-1 py-3 bg-white">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <button
          onClick={handleBack}
          className="p-1 hover:bg-gray-100 rounded-full"
        >
          <ArrowLeft size={20} className="text-gray-600" />
        </button>
        <h2 className="text-xl font-semibold flex items-center gap-2">
          <Zap size={20} className="text-blue-500" />
          Job Analysis
        </h2>
        <div className="w-6" /> {/* Spacer */}
      </div>

      {/* Job Title and Company */}
      <div className="bg-indigo-50 p-6 rounded-lg mb-6">
        <div className="mb-3">
          <h1 className="text-lg font-bold text-gray-900 text-center mb-2">
            {resultsData.title}
          </h1>
          <p className="text-gray-600 text-base text-center">
            {resultsData.company}
          </p>
        </div>

        {/* Summary Section (Brief Overview) */}
        {resultsData.summary && (
          <div className="mb-6">
            <h3 className="text-md font-medium text-gray-800 text-center mb-2">
              Summary
            </h3>
            <p className="text-gray-600 text-sm leading-relaxed text-center px-4">
              {resultsData.summary}
            </p>
          </div>
        )}

        {/* Score Section (Central Focus) */}
        <div className="flex flex-col items-center justify-center">
          <div
            className={`w-24 h-24 rounded-full flex items-center justify-center mb-4 
              ${
                resultsData.score < 50
                  ? "bg-red-400 text-white" // Low compatibility
                  : resultsData.score < 70
                  ? "bg-yellow-500 text-white" // Medium compatibility
                  : resultsData.score < 90
                  ? "bg-green-500 text-white" // High compatibility
                  : "bg-green-500 text-white"
              }`}
          >
            <span className="text-3xl font-bold">{resultsData.score}</span>
          </div>

          <h3 className="text-xl font-semibold text-gray-900 mb-2">
            Compatibility Score
          </h3>
          <p className="text-gray-600 text-sm text-center">
            Your resume matches {resultsData.score}% of the job requirements.
          </p>
        </div>
      </div>

      {/* Job Details */}
      <div className="space-y-6">
        {/* Basic Info */}
        <div className="bg-gray-50 p-4 rounded-lg">
          <div className="grid grid-cols-2 gap-2 text-sm">
            {/* Location with Location Type as Subtext */}
            <div className="flex items-center gap-3">
              <MapPin size={16} className="text-gray-500" />
              <div className="flex flex-col">
                <span>{resultsData.location}</span>
                <div className="flex items-center gap-1 text-xs text-gray-500">
                  <MapPin size={12} className="text-gray-400" />
                  <span>{resultsData.location_type}</span>
                </div>
              </div>
            </div>

            {/* Job Type */}
            <div className="flex items-center gap-2">
              <Briefcase size={16} className="text-gray-500" />
              <span>{resultsData.job_type}</span>
            </div>

            {/* Date Posted */}
            <div className="flex items-center gap-2">
              <Clock size={16} className="text-gray-500" />
              <span>Posted {resultsData.date_posted}</span>
            </div>

            {/* Salary */}
            <div className="flex items-center gap-2">
              <CircleDollarSign size={16} className="text-gray-500" />
              <span>{resultsData.salary}</span>
            </div>
          </div>
        </div>

        {/* Key Details */}
        <div className="space-y-4">
          <Section title="Key Technologies" icon={<ClipboardList size={18} />}>
            <div className="flex flex-wrap gap-2">
              {resultsData.key_technologies?.map((tech, index) => (
                <span
                  key={index}
                  className="bg-blue-100 px-2 py-1 rounded text-sm"
                >
                  {tech}
                </span>
              ))}
            </div>
          </Section>

          <Section title="Required Skills" icon={<Briefcase size={18} />}>
            <div className="flex flex-wrap gap-2">
              {resultsData.key_skills?.map((skill, index) => (
                <span
                  key={index}
                  className="bg-green-100 px-2 py-1 rounded text-sm"
                >
                  {skill}
                </span>
              ))}
            </div>
          </Section>

          <Section title="Analysis" icon={<Lightbulb size={18} />}>
            <p className="text-gray-700 text-sm leading-relaxed">
              {resultsData.matching_analysis}
            </p>
          </Section>

          <Section title="Recommendations" icon={<Star size={18} />}>
            <ul className="list-disc list-outside space-y-2 pl-2">
              {resultsData.recommendations?.map((rec, index) => (
                <li key={index} className="text-sm text-gray-700">
                  {rec}
                </li>
              ))}
            </ul>
          </Section>
        </div>
      </div>
    </div>
  );
};

export default Results;
