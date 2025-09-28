import React, { useRef } from "react";
import { motion } from "framer-motion";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Upload, Image as ImageIcon, FileImage } from "lucide-react";

export default function FileUploadZone({ 
  onFileSelect, 
  title = "Upload Cover Image",
  subtitle = "Choose an image to hide your secret message within"
}) {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = React.useState(false);

  const handleDrag = React.useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = React.useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const files = Array.from(e.dataTransfer.files);
    const imageFile = files.find(file => file.type.startsWith('image/'));
    
    if (imageFile) {
      onFileSelect(imageFile);
    }
  }, [onFileSelect]);

  const handleFileInput = (e) => {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
      onFileSelect(file);
    }
  };

  const handleBrowseClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.2 }}
    >
      <Card 
        className={`border-2 border-dashed transition-colors cursor-pointer ${
          dragActive 
            ? 'border-blue-400 bg-blue-500/10' 
            : 'border-slate-600 bg-slate-700/20 hover:border-slate-500'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={handleBrowseClick}
      >
        <CardContent className="p-12">
          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileInput}
            className="hidden"
          />
          
          <div className="text-center space-y-4">
            <div className="w-20 h-20 bg-slate-600/30 rounded-2xl flex items-center justify-center mx-auto">
              <ImageIcon className="w-10 h-10 text-slate-400" />
            </div>
            
            <div className="space-y-2">
              <h3 className="text-xl font-semibold text-white">{title}</h3>
              <p className="text-slate-400">{subtitle}</p>
            </div>
            
            <div className="space-y-3">
              <Button
                type="button"
                className="bg-blue-600 hover:bg-blue-700"
                onClick={handleBrowseClick}
              >
                <Upload className="w-4 h-4 mr-2" />
                Choose Image File
              </Button>
              
              <p className="text-xs text-slate-500">
                or drag and drop your image here
              </p>
              
              <div className="flex items-center justify-center gap-4 text-xs text-slate-500">
                <div className="flex items-center gap-1">
                  <FileImage className="w-3 h-3" />
                  PNG
                </div>
                <div className="flex items-center gap-1">
                  <FileImage className="w-3 h-3" />
                  JPG
                </div>
                <div className="flex items-center gap-1">
                  <FileImage className="w-3 h-3" />
                  JPEG
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  );
}