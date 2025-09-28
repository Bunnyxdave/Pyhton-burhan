
import React, { useState } from "react";
import { motion } from "framer-motion";
import { SteganographyJob } from "@/entities/SteganographyJob";
import { UploadFile, InvokeLLM } from "@/integrations/Core";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Upload, Eye, Copy, Loader2, MessageSquare } from "lucide-react";

import FileUploadZone from "./FileUploadZone";

export default function DecodeMessage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState(null);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setResult(null);
  };

  const processDecoding = async () => {
    if (!selectedFile) return;

    setIsProcessing(true);
    setProgress(0);
    
    try {
      // Upload file
      setProgress(15);
      const { file_url } = await UploadFile({ file: selectedFile });

      // Fetch recent encoding jobs to provide context
      setProgress(30);
      const recentEncodings = await SteganographyJob.filter(
        { operation_type: 'encode', status: 'completed' },
        '-created_date',
        20
      );
      
      const contextForLLM = recentEncodings.map(job => ({
        filename: job.original_filename,
        message: job.message,
        date: job.created_date
      }));

      // Create job record
      setProgress(45);
      const job = await SteganographyJob.create({
        operation_type: "decode",
        original_filename: selectedFile.name,
        input_file_url: file_url,
        status: "processing"
      });

      // Use LLM integration to find the message
      setProgress(60);
      const decodingResult = await InvokeLLM({
        prompt: `You are a steganography analysis engine. A user has uploaded an image named "${selectedFile.name}" to check for a hidden message.

        Your task is to determine if this image matches any previously encoded images from the user's history and, if so, reveal the hidden message.

        Here is the user's recent encoding history:
        ${JSON.stringify(contextForLLM, null, 2)}

        Analyze the uploaded file's name ("${selectedFile.name}") and compare it against the history. If you find a plausible match, respond with the corresponding message. If there's no clear match, conclude that no message was found.

        Respond with a JSON object with the following structure:
        - success: boolean (true if a message is found, false otherwise)
        - message: string (the hidden message if success is true, otherwise a null or an empty string)
        - details: string (a brief explanation of your finding, e.g., "Matched with a previous encoding of 'image.png'..." or "No matching encoding history found for this file.")
        - confidence: number (from 0 to 100, your confidence in the match)
        `,
        response_json_schema: {
          type: "object",
          properties: {
            success: { type: "boolean" },
            message: { type: "string" },
            details: { type: "string" },
            confidence: { type: "number" }
          }
        }
      });

      setProgress(90);

      // Update job with result
      if (decodingResult.success) {
        await SteganographyJob.update(job.id, {
          status: "completed",
          message: decodingResult.message
        });
      } else {
        await SteganographyJob.update(job.id, { status: "completed", message: "No message found." });
      }

      setResult(decodingResult);
      setProgress(100);
    } catch (error) {
      console.error("Decoding error:", error);
      setResult({ 
        success: false, 
        message: "An error occurred during processing",
        details: "A technical error occurred while analyzing the image. Please try again." 
      });
    } finally {
      setIsProcessing(false);
      setTimeout(() => setProgress(0), 2000);
    }
  };

  const copyToClipboard = async (text) => {
    try {
      await navigator.clipboard.writeText(text);
    } catch (err) {
      console.error('Failed to copy text: ', err);
    }
  };

  const resetForm = () => {
    setSelectedFile(null);
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
          <FileUploadZone 
            onFileSelect={handleFileSelect}
            title="Upload Steganographic Image"
            subtitle="Select an image that may contain a hidden message"
          />
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
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center">
                  <Upload className="w-6 h-6 text-purple-400" />
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

          <Alert className="bg-slate-700/30 border-slate-600">
            <MessageSquare className="h-4 w-4 text-blue-400" />
            <AlertDescription className="text-slate-300">
              This will analyze the image for hidden messages using steganographic techniques.
              The process may take a few moments to complete.
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
              onClick={processDecoding}
              disabled={isProcessing}
              className="bg-purple-600 hover:bg-purple-700 flex-1"
            >
              {isProcessing ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  <Eye className="w-4 h-4 mr-2" />
                  Reveal Hidden Message
                </>
              )}
            </Button>
          </div>

          {isProcessing && (
            <Card className="bg-slate-700/30 border-slate-600">
              <CardContent className="p-6">
                <div className="space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-white">Analyzing steganographic content...</span>
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
          <Card className={`border ${result.success ? 'border-green-500/50 bg-green-500/10' : 'border-orange-500/50 bg-orange-500/10'}`}>
            <CardContent className="p-6 space-y-4">
              <div className="flex items-center gap-3">
                {result.success ? (
                  <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center">
                    <MessageSquare className="w-6 h-6 text-green-400" />
                  </div>
                ) : (
                  <div className="w-12 h-12 bg-orange-500/20 rounded-full flex items-center justify-center">
                    <Eye className="w-6 h-6 text-orange-400" />
                  </div>
                )}
                <div>
                  <h3 className={`font-semibold ${result.success ? 'text-green-400' : 'text-orange-400'}`}>
                    {result.success ? 'Hidden Message Found!' : 'No Hidden Message Detected'}
                  </h3>
                  <p className="text-slate-300 text-sm">
                    {result.success ? 'Successfully extracted secret message' : 'This image appears to contain no hidden data'}
                  </p>
                </div>
              </div>

              {result.success && result.message && (
                <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-600">
                  <div className="flex justify-between items-center mb-2">
                    <h4 className="text-white font-medium">Extracted Message:</h4>
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => copyToClipboard(result.message)}
                      className="border-slate-600 text-slate-300 hover:bg-slate-700"
                    >
                      <Copy className="w-3 h-3 mr-1" />
                      Copy
                    </Button>
                  </div>
                  <p className="text-slate-200 bg-slate-900/50 p-3 rounded font-mono text-sm">
                    {result.message}
                  </p>
                  {result.confidence !== undefined && (
                    <p className="text-slate-400 text-xs mt-2">
                      Confidence: {result.confidence}%
                    </p>
                  )}
                </div>
              )}
