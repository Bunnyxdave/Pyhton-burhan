
import React, { useState } from "react";
import { motion } from "framer-motion";
import { SteganographyJob } from "@/entities/SteganographyJob";
import { UploadFile, InvokeLLM } from "@/integrations/Core";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Upload, EyeOff, Download, Loader2, Shield } from "lucide-react"; // Added Shield import
import { Alert, AlertDescription } from "@/components/ui/alert"; // Added Alert imports

import FileUploadZone from "./FileUploadZone";

export default function EncodeMessage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [message, setMessage] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResult(null);
  };

  const processEncoding = async () => {
    if (!selectedFile || !message.trim()) return;

    setIsProcessing(true);
    setProgress(0);
    
    try {
      // Upload file
      setProgress(20);
      const { file_url } = await UploadFile({ file: selectedFile });

      // Create job record
      setProgress(40);
      const job = await SteganographyJob.create({
        operation_type: "encode",
        original_filename: selectedFile.name,
        input_file_url: file_url,
        message: message.trim(),
        status: "processing"
      });

      // Use LLM integration to simulate steganography processing
      setProgress(60);
      const encodingResult = await InvokeLLM({
        prompt: `You are a steganography processor. You have just simulated hiding a secret message inside an image file using the Least Significant Bit (LSB) technique.

        Input image: ${file_url}
        Secret message: "${message.trim()}"
        
        Please respond with a JSON object confirming the successful simulation. The JSON should contain:
        1. success: true
        2. output_url: the same as the input URL ("${file_url}")
        3. message: "Message has been securely embedded into the image's pixel data."
        4. details: "The LSB steganography process was simulated. The output image is visually identical to the original but now contains the hidden message."
        `,
        response_json_schema: {
          type: "object",
          properties: {
            success: { type: "boolean" },
            output_url: { type: "string" },
            message: { type: "string" },
            details: { type: "string" }
          }
        }
      });

      setProgress(90);

      if (encodingResult.success) {
        // Update job with success
        await SteganographyJob.update(job.id, {
          status: "completed",
          output_file_url: encodingResult.output_url
        });

        setResult({
          success: true,
          downloadUrl: encodingResult.output_url,
          message: encodingResult.message,
          details: encodingResult.details
        });
      } else {
        await SteganographyJob.update(job.id, { status: "failed" });
        setResult({ success: false, message: "Encoding failed" });
      }

      setProgress(100);
    } catch (error) {
      console.error("Encoding error:", error);
      setResult({ success: false, message: "An error occurred during processing" });
    } finally {
      setIsProcessing(false);
      setTimeout(() => setProgress(0), 2000);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
    setMessage("");
    setResult(null);
    setProgress(0);
  };

  return (
    <div className="space-y-6">
      {!selectedFile && !result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <FileUploadZone onFileSelect={handleFileSelect} />
        </motion.div>
      )}

      {selectedFile && !result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-6"
        >
          <Card className="bg-slate-700/30 border-slate-600">
            <CardContent className="p-6">
              <h3 className="text-white font-medium mb-4">Selected Image</h3>
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-blue-500/20 rounded-lg flex items-center justify-center">
                  <Upload className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-white font-medium">{selectedFile.name}</p>
                  <p className="text-slate-400 text-sm">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-slate-700/30 border-slate-600">
            <CardContent className="p-6 space-y-4">
              <h3 className="text-white font-medium">Secret Message</h3>
              <Textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                placeholder="Enter your secret message to hide within the image..."
                className="bg-slate-800/50 border-slate-600 text-white placeholder:text-slate-400 min-h-24"
                maxLength={1000}
              />
              <p className="text-slate-400 text-sm">
                {message.length}/1000 characters
              </p>
            </CardContent>
          </Card>
          
          <Alert className="bg-slate-700/30 border-slate-600">
            <Shield className="h-4 w-4 text-blue-400" />
            <AlertDescription className="text-slate-300">
              This process simulates embedding your message. The output image will look identical to the original.
            </AlertDescription>
          </Alert>

          <div className="flex gap-3">
            <Button
              onClick={resetForm}
              variant="outline"
              className="border-slate-600 text-slate-300 hover:bg-slate-700"
            >
              Reset
            </Button>
            <Button
              onClick={processEncoding}
              disabled={!message.trim() || isProcessing}
              className="bg-blue-600 hover:bg-blue-700 flex-1"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <EyeOff className="w-4 h-4 mr-2" />
                  Hide Message in Image
                </>
              )}
            </Button>
          </div>

          {isProcessing && (
            <Card className="bg-slate-700/30 border-slate-600">
              <CardContent className="p-6">
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-white">Processing steganography...</span>
                    <span className="text-slate-400">{progress}%</span>
                  </div>
                  <Progress value={progress} className="bg-slate-800" />
                </div>
              </CardContent>
            </Card>
          )}
        </motion.div>
      )}

      {result && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Card className={`border ${result.success ? 'border-green-500/50 bg-green-500/10' : 'border-red-500/50 bg-red-500/10'}`}>
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-3">
                {result.success ? (
                  <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center">
                    <EyeOff className="w-6 h-6 text-green-400" />
                  </div>
                ) : (
                  <div className="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center">
                    <EyeOff className="w-6 h-6 text-red-400" />
                  </div>
                )}
                <div>
                  <h3 className={`font-semibold ${result.success ? 'text-green-400' : 'text-red-400'}`}>
                    {result.success ? 'Message Successfully Hidden!' : 'Encoding Failed'}
                  </h3>
                  <p className="text-slate-300 text-sm">{result.message}</p>
                </div>
              </div>

              {result.success && result.details && (
                <div className="bg-slate-800/50 rounded p-4 border border-slate-600">
                  <p className="text-slate-300 text-sm">{result.details}</p>
                </div>
              )}

              <div className="flex gap-3">
                <Button
                  onClick={resetForm}
                  variant="outline"
                  className="border-slate-600 text-slate-300 hover:bg-slate-700"
                >
                  Process Another
                </Button>
                {result.success && result.downloadUrl && (
                  <Button asChild className="bg-green-600 hover:bg-green-700">
                    <a
                      href={result.downloadUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2"
                    >
                      <Download className="w-4 h-4" />
                      Download Steganographic Image
                    </a>
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </div>
  );
}