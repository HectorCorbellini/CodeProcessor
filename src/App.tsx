import React, { useState, useRef, DragEvent } from 'react';
import { FolderOpen, Copy, Save, Bot, FileText } from 'lucide-react';

interface ProcessedFile {
  path: string;
  language: string;
  content: string;
}

function App() {
  const [files, setFiles] = useState<ProcessedFile[]>([]);
  const [preview, setPreview] = useState<string>('');
  const [processedContent, setProcessedContent] = useState<string>('');
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const getFileLanguage = (filename: string): string => {
    const ext = filename.split('.').pop()?.toLowerCase() || '';
    const languageMap: { [key: string]: string } = {
      java: 'Java',
      py: 'Python',
      html: 'HTML',
      htm: 'HTML',
      js: 'JavaScript',
      css: 'CSS',
      xml: 'XML',
      sql: 'SQL',
      json: 'JSON',
      properties: 'Properties',
      jsp: 'JSP'
    };
    return languageMap[ext] || 'Plain Text';
  };

  const processSelectedFiles = async (items: DataTransferItemList | FileList) => {
    const validExtensions = ['.java', '.py', '.html', '.htm', '.js', '.css', '.xml', '.sql', '.json', '.properties', '.jsp'];
    const processedFiles: ProcessedFile[] = [];
    
    const processEntry = async (entry: FileSystemEntry) => {
      if (entry.isFile) {
        const fileEntry = entry as FileSystemFileEntry;
        return new Promise<void>((resolve) => {
          fileEntry.file(async (file) => {
            if (validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))) {
              const content = await file.text();
              processedFiles.push({
                path: (file as any).webkitRelativePath || file.name,
                language: getFileLanguage(file.name),
                content
              });
            }
            resolve();
          });
        });
      } else if (entry.isDirectory) {
        const dirEntry = entry as FileSystemDirectoryEntry;
        const dirReader = dirEntry.createReader();
        return new Promise<void>((resolve) => {
          const readEntries = async () => {
            dirReader.readEntries(async (entries) => {
              if (entries.length === 0) {
                resolve();
                return;
              }
              await Promise.all(entries.map(processEntry));
              readEntries();
            });
          };
          readEntries();
        });
      }
    };

    if (items instanceof DataTransferItemList) {
      for (let i = 0; i < items.length; i++) {
        const entry = items[i].webkitGetAsEntry();
        if (entry) {
          await processEntry(entry);
        }
      }
    } else {
      // Handle FileList (from input element)
      for (const file of Array.from(items)) {
        if (validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))) {
          const content = await file.text();
          processedFiles.push({
            path: file.webkitRelativePath || file.name,
            language: getFileLanguage(file.name),
            content
          });
        }
      }
    }

    setFiles(processedFiles.sort((a, b) => a.path.localeCompare(b.path)));
    if (processedFiles.length > 0) {
      setPreview(processedFiles[0].content.slice(0, 200) + '...');
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      await processSelectedFiles(e.target.files);
    }
  };

  const handleDragEnter = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = async (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const items = e.dataTransfer.items;
    await processSelectedFiles(items);
  };

  const processFiles = () => {
    const result = files.map(file => (
      `// === FILE: ${file.path} ===\n` +
      `// === LANGUAGE: ${file.language}\n\n` +
      `${file.content}\n\n` +
      '-'.repeat(50) + '\n'
    )).join('\n');
    
    setProcessedContent(result);
    navigator.clipboard.writeText(result);
  };

  const saveToFile = () => {
    const blob = new Blob([processedContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'processed-code.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  const openAI = (platform: string) => {
    const urls: { [key: string]: string } = {
      'ChatGPT': 'https://chat.openai.com',
      'Gemini': 'https://gemini.google.com',
      'Claude': 'https://claude.ai',
      'Copilot': 'https://copilot.microsoft.com'
    };
    window.open(urls[platform], '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-8 flex items-center gap-2">
            <FileText className="w-8 h-8 text-blue-600" />
            Code Processor for AI
          </h1>

          <div className="space-y-6">
            {/* File Selection */}
            <div
              className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                isDragging
                  ? 'border-blue-500 bg-blue-50'
                  : 'border-gray-300 hover:border-gray-400'
              }`}
              onDragEnter={handleDragEnter}
              onDragLeave={handleDragLeave}
              onDragOver={handleDragOver}
              onDrop={handleDrop}
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                webkitdirectory=""
                directory=""
                multiple
                className="hidden"
              />
              <div className="flex flex-col items-center gap-3">
                <button
                  onClick={() => fileInputRef.current?.click()}
                  className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                  <FolderOpen className="w-5 h-5" />
                  Select Directory
                </button>
                <p className="text-sm text-gray-600">
                  or drag and drop a directory here
                </p>
                <p className="text-sm text-gray-500">
                  {files.length > 0 ? `${files.length} files selected` : 'No files selected'}
                </p>
              </div>
            </div>

            {/* Preview */}
            {preview && (
              <div className="bg-gray-50 rounded-lg p-4">
                <h2 className="text-lg font-semibold mb-2">Preview:</h2>
                <pre className="text-sm text-gray-700 overflow-x-auto">
                  {preview}
                </pre>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-4">
              <button
                onClick={processFiles}
                disabled={files.length === 0}
                className="flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Copy className="w-5 h-5" />
                Process & Copy
              </button>
              
              <button
                onClick={saveToFile}
                disabled={!processedContent}
                className="flex items-center gap-2 px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save className="w-5 h-5" />
                Save as TXT
              </button>
            </div>

            {/* AI Platforms */}
            <div className="border-t pt-6 mt-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Bot className="w-5 h-5 text-gray-700" />
                Open in AI Platform
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {['ChatGPT', 'Gemini', 'Claude', 'Copilot'].map((platform) => (
                  <button
                    key={platform}
                    onClick={() => openAI(platform)}
                    className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                  >
                    {platform}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;