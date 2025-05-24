# Oslo Planning Dashboard - Comprehensive Development Plan
## Standalone Software System Evolution

### Executive Summary
This document outlines the transformation of the existing Oslo planning dashboard into a fully standalone software system capable of operating independently without external APIs, while maintaining preparation for future API integration.

## 1. Project Structure Overview

```
oslo-planning-dashboard/
├── frontend/                    # React TypeScript Frontend
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── stores/            # State management (Zustand)
│   │   ├── services/          # Data services
│   │   ├── utils/             # Utility functions
│   │   ├── types/             # TypeScript definitions
│   │   ├── hooks/             # Custom React hooks
│   │   └── assets/            # Static assets
│   ├── public/
│   └── package.json
├── backend/                     # Node.js/Express Backend
│   ├── src/
│   │   ├── routes/            # API routes
│   │   ├── models/            # Data models
│   │   ├── services/          # Business logic
│   │   ├── middleware/        # Express middleware
│   │   ├── utils/             # Utility functions
│   │   └── db/                # Database configurations
│   └── package.json
├── database/                    # Database setup
│   ├── migrations/            # Database migrations
│   ├── seeds/                 # Sample data
│   └── schemas/               # Database schemas
├── ai-ml/                      # AI/ML Components
│   ├── models/                # ML models
│   ├── training/              # Training scripts
│   └── inference/             # Inference engines
├── mobile/                     # React Native mobile app
├── desktop/                    # Electron desktop app
├── docs/                       # Documentation
├── tests/                      # Testing suites
└── docker/                     # Docker configurations
```

## 2. Technology Stack

### Frontend Stack
- **React 18** with TypeScript
- **Vite** for build tooling
- **Tailwind CSS** for styling
- **Zustand** for state management
- **React Query** for data fetching
- **D3.js** for advanced visualizations
- **Mapbox GL JS** for mapping
- **Chart.js** for charts
- **React Hook Form** for forms

### Backend Stack
- **Node.js** with Express
- **TypeScript** for type safety
- **PostgreSQL** with PostGIS for spatial data
- **Redis** for caching
- **Socket.io** for real-time features
- **Multer** for file uploads
- **Sharp** for image processing

### AI/ML Stack
- **TensorFlow.js** for client-side ML
- **Python** backend for complex ML
- **scikit-learn** for data analysis
- **pandas** for data manipulation
- **OpenAI GPT** integration (when available)

### Infrastructure
- **Docker** for containerization
- **Nginx** for reverse proxy
- **PM2** for process management
- **Winston** for logging

## 3. Detailed Implementation Plan

### 3.1 Local Data Storage and Management System

#### Database Schema Design

```sql
-- Core entities
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    location_name VARCHAR(255),
    geometry GEOMETRY(POLYGON, 4326),
    status project_status DEFAULT 'planning',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE regulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    type regulation_type NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT,
    effective_date DATE,
    expires_date DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    filename VARCHAR(255) NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    file_size BIGINT,
    content_text TEXT, -- Extracted text content
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE spatial_layers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    type layer_type NOT NULL,
    geometry_type VARCHAR(50),
    data JSONB, -- GeoJSON data
    style JSONB, -- Layer styling
    visible BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### Data Management Service

```typescript
// backend/src/services/DataManager.ts
import { Pool } from 'pg';
import { Redis } from 'ioredis';

export class DataManager {
    private db: Pool;
    private cache: Redis;

    constructor() {
        this.db = new Pool({
            connectionString: process.env.DATABASE_URL,
        });
        this.cache = new Redis(process.env.REDIS_URL);
    }

    async importData(file: Express.Multer.File, type: 'geojson' | 'csv' | 'excel' | 'pdf') {
        switch (type) {
            case 'geojson':
                return this.importGeoJSON(file);
            case 'csv':
                return this.importCSV(file);
            case 'excel':
                return this.importExcel(file);
            case 'pdf':
                return this.importPDF(file);
        }
    }

    private async importGeoJSON(file: Express.Multer.File) {
        const content = JSON.parse(file.buffer.toString());
        const features = content.features || [content];
        
        for (const feature of features) {
            await this.db.query(`
                INSERT INTO spatial_layers (name, type, geometry_type, data)
                VALUES ($1, $2, $3, $4)
            `, [
                feature.properties?.name || 'Imported Layer',
                'user_imported',
                feature.geometry.type,
                JSON.stringify(feature)
            ]);
        }
    }

    async exportData(projectId: string, format: 'geojson' | 'csv' | 'pdf') {
        const project = await this.getProject(projectId);
        
        switch (format) {
            case 'geojson':
                return this.exportToGeoJSON(project);
            case 'csv':
                return this.exportToCSV(project);
            case 'pdf':
                return this.exportToPDF(project);
        }
    }

    async syncOfflineData() {
        // Sync data when connection is restored
        const offlineData = await this.cache.get('offline_changes');
        if (offlineData) {
            const changes = JSON.parse(offlineData);
            for (const change of changes) {
                await this.applyChange(change);
            }
            await this.cache.del('offline_changes');
        }
    }
}
```

### 3.2 Advanced Graphics and Visualization Improvements

#### Interactive Map Component

```typescript
// frontend/src/components/Map/InteractiveMap.tsx
import React, { useEffect, useRef, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import { useMapStore } from '../stores/mapStore';

interface InteractiveMapProps {
    onFeatureClick?: (feature: any) => void;
    onDrawComplete?: (feature: any) => void;
}

export const InteractiveMap: React.FC<InteractiveMapProps> = ({
    onFeatureClick,
    onDrawComplete
}) => {
    const mapContainer = useRef<HTMLDivElement>(null);
    const map = useRef<mapboxgl.Map | null>(null);
    const { layers, selectedLayer, mapStyle, filters } = useMapStore();

    useEffect(() => {
        if (!mapContainer.current) return;

        // Initialize map
        map.current = new mapboxgl.Map({
            container: mapContainer.current,
            style: mapStyle || 'mapbox://styles/mapbox/streets-v11',
            center: [10.7522, 59.9139], // Oslo coordinates
            zoom: 10,
            pitch: 45,
            bearing: -15
        });

        // Add 3D buildings
        map.current.on('style.load', () => {
            const layers = map.current!.getStyle().layers;
            const labelLayerId = layers.find(
                layer => layer.type === 'symbol' && layer.layout?.['text-field']
            )?.id;

            map.current!.addLayer({
                id: '3d-buildings',
                source: 'composite',
                'source-layer': 'building',
                filter: ['==', 'extrude', 'true'],
                type: 'fill-extrusion',
                minzoom: 15,
                paint: {
                    'fill-extrusion-color': '#aaa',
                    'fill-extrusion-height': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15, 0,
                        15.05, ['get', 'height']
                    ],
                    'fill-extrusion-base': [
                        'interpolate',
                        ['linear'],
                        ['zoom'],
                        15, 0,
                        15.05, ['get', 'min_height']
                    ],
                    'fill-extrusion-opacity': 0.8
                }
            }, labelLayerId);
        });

        // Add drawing controls
        const draw = new MapboxDraw({
            displayControlsDefault: false,
            controls: {
                polygon: true,
                point: true,
                line_string: true,
                trash: true
            }
        });
        
        map.current.addControl(draw);

        map.current.on('draw.create', (e) => {
            onDrawComplete?.(e.features[0]);
        });

        // Cleanup
        return () => {
            map.current?.remove();
        };
    }, []);

    // Update layers when store changes
    useEffect(() => {
        if (!map.current) return;

        layers.forEach(layer => {
            if (layer.visible && !map.current!.getLayer(layer.id)) {
                addLayerToMap(layer);
            } else if (!layer.visible && map.current!.getLayer(layer.id)) {
                map.current!.removeLayer(layer.id);
                if (map.current!.getSource(layer.id)) {
                    map.current!.removeSource(layer.id);
                }
            }
        });
    }, [layers]);

    const addLayerToMap = (layer: any) => {
        if (!map.current) return;

        map.current.addSource(layer.id, {
            type: 'geojson',
            data: layer.data
        });

        map.current.addLayer({
            id: layer.id,
            type: layer.type,
            source: layer.id,
            paint: layer.style.paint,
            layout: layer.style.layout
        });
    };

    return (
        <div className="relative w-full h-full">
            <div ref={mapContainer} className="w-full h-full" />
            
            {/* Map controls */}
            <div className="absolute top-4 right-4 bg-white rounded-lg shadow-lg p-4">
                <LayerControl />
                <FilterControl />
                <StyleControl />
            </div>
        </div>
    );
};
```

#### Advanced Chart Components

```typescript
// frontend/src/components/Charts/AdvancedCharts.tsx
import React from 'react';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement,
} from 'chart.js';
import { Line, Bar, Doughnut, Scatter } from 'react-chartjs-2';
import * as d3 from 'd3';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

export const TimeSeriesChart: React.FC<{ data: any[] }> = ({ data }) => {
    const chartData = {
        labels: data.map(d => d.date),
        datasets: [
            {
                label: 'Planning Applications',
                data: data.map(d => d.applications),
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.4,
            },
            {
                label: 'Approvals',
                data: data.map(d => d.approvals),
                borderColor: 'rgb(54, 162, 235)',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                tension: 0.4,
            }
        ],
    };

    const options = {
        responsive: true,
        interaction: {
            mode: 'index' as const,
            intersect: false,
        },
        plugins: {
            title: {
                display: true,
                text: 'Planning Activity Over Time',
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: 'white',
                bodyColor: 'white',
            },
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Date'
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: 'Count'
                }
            }
        },
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart' as const,
        }
    };

    return <Line data={chartData} options={options} />;
};

export const D3TreeMap: React.FC<{ data: any }> = ({ data }) => {
    const ref = useRef<SVGSVGElement>(null);

    useEffect(() => {
        if (!ref.current || !data) return;

        const svg = d3.select(ref.current);
        svg.selectAll("*").remove();

        const width = 800;
        const height = 600;

        const hierarchy = d3.hierarchy(data)
            .sum(d => d.value)
            .sort((a, b) => b.value! - a.value!);

        const treemap = d3.treemap()
            .size([width, height])
            .padding(1);

        const root = treemap(hierarchy);

        const color = d3.scaleOrdinal(d3.schemeCategory10);

        const cell = svg.selectAll("g")
            .data(root.leaves())
            .enter().append("g")
            .attr("transform", d => `translate(${d.x0},${d.y0})`);

        cell.append("rect")
            .attr("width", d => d.x1 - d.x0)
            .attr("height", d => d.y1 - d.y0)
            .attr("fill", d => color(d.parent!.data.name))
            .attr("stroke", "white")
            .attr("stroke-width", 2);

        cell.append("text")
            .attr("x", 4)
            .attr("y", 20)
            .text(d => d.data.name)
            .attr("font-size", "12px")
            .attr("fill", "white");

    }, [data]);

    return <svg ref={ref} width={800} height={600} />;
};
```

### 3.3 Data Input/Import Capabilities

#### File Upload Component

```typescript
// frontend/src/components/Upload/FileUpload.tsx
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { toast } from 'react-hot-toast';

interface FileUploadProps {
    onUpload: (files: File[]) => Promise<void>;
    acceptedFileTypes?: string[];
    maxFileSize?: number;
}

export const FileUpload: React.FC<FileUploadProps> = ({
    onUpload,
    acceptedFileTypes = ['.geojson', '.csv', '.xlsx', '.pdf', '.shp'],
    maxFileSize = 100 * 1024 * 1024 // 100MB
}) => {
    const [uploading, setUploading] = useState(false);
    const [uploadProgress, setUploadProgress] = useState<Record<string, number>>({});

    const onDrop = useCallback(async (acceptedFiles: File[]) => {
        setUploading(true);
        
        try {
            // Validate files
            for (const file of acceptedFiles) {
                if (file.size > maxFileSize) {
                    toast.error(`File ${file.name} is too large (max ${maxFileSize / 1024 / 1024}MB)`);
                    return;
                }
            }

            // Upload files with progress tracking
            await Promise.all(
                acceptedFiles.map(async (file, index) => {
                    const formData = new FormData();
                    formData.append('file', file);
                    formData.append('type', getFileType(file.name));

                    const xhr = new XMLHttpRequest();
                    
                    return new Promise((resolve, reject) => {
                        xhr.upload.addEventListener('progress', (e) => {
                            if (e.lengthComputable) {
                                const progress = (e.loaded / e.total) * 100;
                                setUploadProgress(prev => ({
                                    ...prev,
                                    [file.name]: progress
                                }));
                            }
                        });

                        xhr.addEventListener('load', () => {
                            if (xhr.status === 200) {
                                toast.success(`Uploaded ${file.name}`);
                                resolve(xhr.response);
                            } else {
                                toast.error(`Failed to upload ${file.name}`);
                                reject(new Error(`Upload failed: ${xhr.status}`));
                            }
                        });

                        xhr.addEventListener('error', () => {
                            toast.error(`Failed to upload ${file.name}`);
                            reject(new Error('Upload failed'));
                        });

                        xhr.open('POST', '/api/upload');
                        xhr.send(formData);
                    });
                })
            );

            toast.success('All files uploaded successfully!');
        } catch (error) {
            console.error('Upload error:', error);
            toast.error('Upload failed');
        } finally {
            setUploading(false);
            setUploadProgress({});
        }
    }, [maxFileSize]);

    const { getRootProps, getInputProps, isDragActive, isDragReject } = useDropzone({
        onDrop,
        accept: {
            'application/json': ['.geojson'],
            'text/csv': ['.csv'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
            'application/pdf': ['.pdf'],
            'application/octet-stream': ['.shp', '.dbf', '.shx', '.prj']
        },
        maxSize: maxFileSize,
        multiple: true
    });

    const getFileType = (filename: string): string => {
        const ext = filename.toLowerCase().split('.').pop();
        switch (ext) {
            case 'geojson': return 'geojson';
            case 'csv': return 'csv';
            case 'xlsx': case 'xls': return 'excel';
            case 'pdf': return 'pdf';
            case 'shp': return 'shapefile';
            default: return 'unknown';
        }
    };

    return (
        <div className="w-full">
            <div
                {...getRootProps()}
                className={`
                    border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
                    ${isDragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'}
                    ${isDragReject ? 'border-red-500 bg-red-50' : ''}
                    ${uploading ? 'pointer-events-none opacity-50' : ''}
                `}
            >
                <input {...getInputProps()} />
                
                <div className="space-y-4">
                    <div className="text-4xl">📁</div>
                    
                    {isDragActive ? (
                        <p className="text-blue-600">Drop the files here...</p>
                    ) : (
                        <div>
                            <p className="text-gray-600 mb-2">
                                Drag & drop files here, or click to select
                            </p>
                            <p className="text-sm text-gray-500">
                                Supports: GeoJSON, CSV, Excel, PDF, Shapefile
                            </p>
                        </div>
                    )}
                </div>
            </div>

            {/* Upload Progress */}
            {Object.keys(uploadProgress).length > 0 && (
                <div className="mt-4 space-y-2">
                    {Object.entries(uploadProgress).map(([filename, progress]) => (
                        <div key={filename} className="bg-gray-100 rounded p-3">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-sm font-medium">{filename}</span>
                                <span className="text-sm text-gray-500">{Math.round(progress)}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                                <div
                                    className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                    style={{ width: `${progress}%` }}
                                />
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};
```

#### Data Processing Service

```typescript
// backend/src/services/DataProcessor.ts
import * as XLSX from 'xlsx';
import pdf from 'pdf-parse';
import shapefile from 'shapefile';

export class DataProcessor {
    async processCSV(buffer: Buffer): Promise<any[]> {
        const text = buffer.toString('utf-8');
        const lines = text.split('\n');
        const headers = lines[0].split(',').map(h => h.trim());
        
        return lines.slice(1).map(line => {
            const values = line.split(',');
            const record: any = {};
            headers.forEach((header, index) => {
                record[header] = values[index]?.trim();
            });
            return record;
        }).filter(record => Object.values(record).some(v => v));
    }

    async processExcel(buffer: Buffer): Promise<any[]> {
        const workbook = XLSX.read(buffer, { type: 'buffer' });
        const worksheet = workbook.Sheets[workbook.SheetNames[0]];
        return XLSX.utils.sheet_to_json(worksheet);
    }

    async processPDF(buffer: Buffer): Promise<{ text: string; metadata: any }> {
        const data = await pdf(buffer);
        return {
            text: data.text,
            metadata: {
                pages: data.numpages,
                info: data.info,
                metadata: data.metadata
            }
        };
    }

    async processShapefile(buffer: Buffer): Promise<any> {
        // Note: In reality, you'd need to handle the entire shapefile package
        const source = await shapefile.read(buffer);
        const features = [];
        
        let result = await source.read();
        while (!result.done) {
            features.push(result.value);
            result = await source.read();
        }
        
        return {
            type: 'FeatureCollection',
            features
        };
    }

    async processGeoJSON(buffer: Buffer): Promise<any> {
        const text = buffer.toString('utf-8');
        const geojson = JSON.parse(text);
        
        // Validate GeoJSON structure
        if (!geojson.type || (geojson.type !== 'FeatureCollection' && geojson.type !== 'Feature')) {
            throw new Error('Invalid GeoJSON format');
        }
        
        return geojson;
    }

    async detectCoordinateSystem(geometry: any): Promise<string> {
        // Simple heuristic to detect coordinate system
        if (geometry.coordinates) {
            const coords = geometry.coordinates.flat(2);
            const minX = Math.min(...coords.filter((_, i) => i % 2 === 0));
            const maxX = Math.max(...coords.filter((_, i) => i % 2 === 0));
            const minY = Math.min(...coords.filter((_, i) => i % 2 === 1));
            const maxY = Math.max(...coords.filter((_, i) => i % 2 === 1));
            
            // Check if coordinates are in Norway area (rough bounds)
            if (minX >= 4 && maxX <= 32 && minY >= 58 && maxY <= 72) {
                return 'EPSG:4326'; // WGS84
            } else if (minX >= 200000 && maxX <= 900000 && minY >= 6400000 && maxY <= 7900000) {
                return 'EPSG:25833'; // UTM Zone 33N
            }
        }
        
        return 'EPSG:4326'; // Default to WGS84
    }
}
```

### 3.4 AI/ML Integration for Analysis Processes

#### Machine Learning Service

```typescript
// backend/src/services/MLAnalysisService.ts
import * as tf from '@tensorflow/tfjs-node';
import { PythonShell } from 'python-shell';

export class MLAnalysisService {
    private models: Map<string, tf.LayersModel> = new Map();

    async loadModels() {
        // Load pre-trained models
        try {
            const planningModel = await tf.loadLayersModel('file://./models/planning-classifier/model.json');
            this.models.set('planning-classifier', planningModel);
            
            const spatialModel = await tf.loadLayersModel('file://./models/spatial-analysis/model.json');
            this.models.set('spatial-analysis', spatialModel);
        } catch (error) {
            console.warn('Could not load ML models:', error);
        }
    }

    async analyzePlanningDocument(text: string): Promise<{
        category: string;
        confidence: number;
        entities: Array<{ text: string; label: string; confidence: number }>;
        summary: string;
    }> {
        // Use Python backend for complex NLP
        const options = {
            mode: 'text' as const,
            pythonPath: 'python3',
            pythonOptions: ['-u'],
            scriptPath: './ai-ml/scripts/',
            args: [text]
        };

        try {
            const results = await PythonShell.run('analyze_document.py', options);
            return JSON.parse(results[0]);
        } catch (error) {
            console.error('Python analysis failed:', error);
            
            // Fallback to simple JS analysis
            return this.fallbackTextAnalysis(text);
        }
    }

    private fallbackTextAnalysis(text: string): any {
        const keywords = {
            'zoning': ['reguleringsplan', 'soneinndeling', 'arealbruk'],
            'environmental': ['miljø', 'forurensning', 'klima', 'natur'],
            'transport': ['transport', 'trafikk', 'kollektivtransport', 'vei'],
            'housing': ['bolig', 'boliger', 'bebyggelse', 'utbygging']
        };

        const scores: Record<string, number> = {};
        
        Object.entries(keywords).forEach(([category, words]) => {
            scores[category] = words.reduce((score, word) => {
                const matches = (text.toLowerCase().match(new RegExp(word, 'g')) || []).length;
                return score + matches;
            }, 0);
        });

        const topCategory = Object.entries(scores).reduce((a, b) => 
            scores[a[0]] > scores[b[0]] ? a : b
        );

        return {
            category: topCategory[0],
            confidence: Math.min(topCategory[1] / 10, 1),
            entities: [],
            summary: text.substring(0, 200) + '...'
        };
    }

    async spatialAnalysis(geojson: any): Promise<{
        area: number;
        centroid: [number, number];
        complexity: number;
        landUseRecommendations: string[];
    }> {
        const model = this.models.get('spatial-analysis');
        
        if (model && geojson.features) {
            // Prepare spatial features for ML model
            const features = this.extractSpatialFeatures(geojson);
            const prediction = model.predict(tf.tensor2d([features])) as tf.Tensor;
            const result = await prediction.data();
            
            return {
                area: this.calculateArea(geojson),
                centroid: this.calculateCentroid(geojson),
                complexity: result[0],
                landUseRecommendations: this.generateRecommendations(result)
            };
        }

        // Fallback to basic geometric analysis
        return {
            area: this.calculateArea(geojson),
            centroid: this.calculateCentroid(geojson),
            complexity: 0.5,
            landUseRecommendations: ['Basic analysis only - ML model not available']
        };
    }

    private extractSpatialFeatures(geojson: any): number[] {
        const features = [];
        
        // Extract basic geometric features
        features.push(this.calculateArea(geojson));
        features.push(this.calculatePerimeter(geojson));
        features.push(geojson.features?.length || 0);
        
        // Add more sophisticated features as needed
        return features;
    }

    private calculateArea(geojson: any): number {
        // Simplified area calculation
        if (!geojson.features) return 0;
        
        return geojson.features.reduce((total: number, feature: any) => {
            if (feature.geometry.type === 'Polygon') {
                // Very basic area calculation - would use proper geospatial library in production
                const coords = feature.geometry.coordinates[0];
                let area = 0;
                for (let i = 0; i < coords.length - 1; i++) {
                    area += coords[i][0] * coords[i + 1][1] - coords[i + 1][0] * coords[i][1];
                }
                return total + Math.abs(area) / 2;
            }
            return total;
        }, 0);
    }

    private calculateCentroid(geojson: any): [number, number] {
        if (!geojson.features || geojson.features.length === 0) return [0, 0];
        
        const allCoords = geojson.features.flatMap((feature: any) => {
            if (feature.geometry.coordinates) {
                return feature.geometry.coordinates.flat(2);
            }
            return [];
        });
        
        const coords = [];
        for (let i = 0; i < allCoords.length; i += 2) {
            coords.push([allCoords[i], allCoords[i + 1]]);
        }
        
        const x = coords.reduce((sum, coord) => sum + coord[0], 0) / coords.length;
        const y = coords.reduce((sum, coord) => sum + coord[1], 0) / coords.length;
        
        return [x, y];
    }

    private calculatePerimeter(geojson: any): number {
        // Simplified perimeter calculation
        return 0; // Implementation would go here
    }

    private generateRecommendations(mlResults: Float32Array): string[] {
        const recommendations = [];
        
        if (mlResults[0] > 0.7) {
            recommendations.push('Suitable for high-density development');
        } else if (mlResults[0] > 0.4) {
            recommendations.push('Suitable for medium-density development');
        } else {
            recommendations.push('Consider low-density or green space development');
        }
        
        return recommendations;
    }
}
```

#### Python ML Scripts

```python
# ai-ml/scripts/analyze_document.py
import sys
import json
import spacy
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

def analyze_document(text):
    try:
        # Load Norwegian language model if available
        try:
            nlp = spacy.load("nb_core_news_sm")
        except:
            nlp = spacy.load("en_core_web_sm")
        
        # Process text
        doc = nlp(text)
        
        # Extract entities
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "confidence": 0.8  # spaCy doesn't provide confidence scores by default
            })
        
        # Classification using transformers
        classifier = pipeline("text-classification", 
                            model="distilbert-base-uncased-finetuned-sst-2-english")
        
        # Categorize based on keywords (simplified)
        planning_keywords = {
            'zoning': ['reguleringsplan', 'soneinndeling', 'arealbruk', 'zoning'],
            'environmental': ['miljø', 'environment', 'klima', 'climate'],
            'transport': ['transport', 'trafikk', 'traffic', 'kollektiv'],
            'housing': ['bolig', 'housing', 'bebyggelse', 'development']
        }
        
        category_scores = {}
        text_lower = text.lower()
        
        for category, keywords in planning_keywords.items():
            score = sum(text_lower.count(keyword) for keyword in keywords)
            category_scores[category] = score
        
        best_category = max(category_scores, key=category_scores.get)
        confidence = min(category_scores[best_category] / 10, 1.0)
        
        # Generate summary (first 200 characters)
        summary = text[:200] + "..." if len(text) > 200 else text
        
        result = {
            "category": best_category,
            "confidence": confidence,
            "entities": entities[:10],  # Limit to top 10 entities
            "summary": summary
        }
        
        return json.dumps(result)
        
    except Exception as e:
        # Fallback result
        return json.dumps({
            "category": "unknown",
            "confidence": 0.0,
            "entities": [],
            "summary": text[:200] + "..." if len(text) > 200 else text,
            "error": str(e)
        })

if __name__ == "__main__":
    input_text = sys.argv[1] if len(sys.argv) > 1 else ""
    result = analyze_document(input_text)
    print(result)
```

### 3.5 Offline-First Architecture

#### Service Worker Implementation

```typescript
// frontend/public/sw.js
const CACHE_NAME = 'oslo-planning-v1';
const urlsToCache = [
    '/',
    '/static/js/bundle.js',
    '/static/css/main.css',
    '/manifest.json'
];

// Install service worker
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(urlsToCache))
    );
});

// Fetch event - implement cache-first strategy
self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request)
            .then((response) => {
                // Return cached version or fetch from network
                if (response) {
                    return response;
                }
                
                return fetch(event.request).then((response) => {
                    // Don't cache if not a valid response
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }
                    
                    const responseToCache = response.clone();
                    caches.open(CACHE_NAME)
                        .then((cache) => {
                            cache.put(event.request, responseToCache);
                        });
                    
                    return response;
                });
            })
    );
});

// Background sync for offline data
self.addEventListener('sync', (event) => {
    if (event.tag === 'background-sync') {
        event.waitUntil(doBackgroundSync());
    }
});

async function doBackgroundSync() {
    // Sync offline changes when connection is restored
    const offlineChanges = await getOfflineChanges();
    
    for (const change of offlineChanges) {
        try {
            await fetch('/api/sync', {
                method: 'POST',
                body: JSON.stringify(change),
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            // Remove from offline storage after successful sync
            await removeOfflineChange(change.id);
        } catch (error) {
            console.error('Sync failed for change:', change.id, error);
        }
    }
}
```

#### Offline Data Store

```typescript
// frontend/src/stores/offlineStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface OfflineState {
    isOnline: boolean;
    pendingChanges: any[];
    cachedData: Record<string, any>;
    addPendingChange: (change: any) => void;
    removePendingChange: (id: string) => void;
    updateOnlineStatus: (status: boolean) => void;
    cacheData: (key: string, data: any) => void;
    getCachedData: (key: string) => any;
}

export const useOfflineStore = create<OfflineState>()(
    persist(
        (set, get) => ({
            isOnline: navigator.onLine,
            pendingChanges: [],
            cachedData: {},
            
            addPendingChange: (change) => {
                set((state) => ({
                    pendingChanges: [...state.pendingChanges, {
                        ...change,
                        id: Date.now().toString(),
                        timestamp: new Date().toISOString()
                    }]
                }));
            },
            
            removePendingChange: (id) => {
                set((state) => ({
                    pendingChanges: state.pendingChanges.filter(change => change.id !== id)
                }));
            },
            
            updateOnlineStatus: (status) => {
                set({ isOnline: status });
                
                // If we're back online, trigger sync
                if (status && get().pendingChanges.length > 0) {
                    navigator.serviceWorker.ready.then((registration) => {
                        return registration.sync.register('background-sync');
                    });
                }
            },
            
            cacheData: (key, data) => {
                set((state) => ({
                    cachedData: {
                        ...state.cachedData,
                        [key]: {
                            data,
                            timestamp: new Date().toISOString()
                        }
                    }
                }));
            },
            
            getCachedData: (key) => {
                const cached = get().cachedData[key];
                if (!cached) return null;
                
                // Check if data is still fresh (24 hours)
                const age = Date.now() - new Date(cached.timestamp).getTime();
                if (age > 24 * 60 * 60 * 1000) {
                    return null;
                }
                
                return cached.data;
            }
        }),
        {
            name: 'oslo-planning-offline',
            partialize: (state) => ({
                pendingChanges: state.pendingChanges,
                cachedData: state.cachedData
            })
        }
    )
);

// Listen for online/offline events
window.addEventListener('online', () => {
    useOfflineStore.getState().updateOnlineStatus(true);
});

window.addEventListener('offline', () => {
    useOfflineStore.getState().updateOnlineStatus(false);
});
```

### 3.6 User Interface Enhancements

#### Modern Dashboard Layout

```typescript
// frontend/src/components/Dashboard/ModernDashboard.tsx
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
    ChartBarIcon, 
    MapIcon, 
    DocumentIcon, 
    CogIcon,
    BellIcon,
    UserIcon 
} from '@heroicons/react/24/outline';

interface DashboardProps {
    user?: any;
}

export const ModernDashboard: React.FC<DashboardProps> = ({ user }) => {
    const [activeTab, setActiveTab] = useState('overview');
    const [notifications, setNotifications] = useState([]);

    const tabs = [
        { id: 'overview', label: 'Oversikt', icon: ChartBarIcon },
        { id: 'map', label: 'Kart', icon: MapIcon },
        { id: 'documents', label: 'Dokumenter', icon: DocumentIcon },
        { id: 'settings', label: 'Innstillinger', icon: CogIcon }
    ];

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center">
                            <div className="flex-shrink-0">
                                <h1 className="text-2xl font-bold text-gray-900">
                                    Oslo Planning Dashboard
                                </h1>
                            </div>
                        </div>
                        
                        <div className="flex items-center space-x-4">
                            <NotificationBell notifications={notifications} />
                            <UserProfile user={user} />
                        </div>
                    </div>
                </div>
            </header>

            <div className="flex">
                {/* Sidebar */}
                <nav className="bg-white shadow-sm w-64 min-h-screen">
                    <div className="p-4">
                        <div className="space-y-2">
                            {tabs.map((tab) => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`
                                        w-full flex items-center px-3 py-2 text-left rounded-lg transition-colors
                                        ${activeTab === tab.id
                                            ? 'bg-blue-100 text-blue-700'
                                            : 'text-gray-600 hover:bg-gray-100'
                                        }
                                    `}
                                >
                                    <tab.icon className="h-5 w-5 mr-3" />
                                    {tab.label}
                                </button>
                            ))}
                        </div>
                    </div>
                </nav>

                {/* Main Content */}
                <main className="flex-1 p-6">
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={activeTab}
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20 }}
                            transition={{ duration: 0.2 }}
                        >
                            {renderTabContent(activeTab)}
                        </motion.div>
                    </AnimatePresence>
                </main>
            </div>
        </div>
    );
};

const renderTabContent = (tab: string) => {
    switch (tab) {
        case 'overview':
            return <OverviewTab />;
        case 'map':
            return <MapTab />;
        case 'documents':
            return <DocumentsTab />;
        case 'settings':
            return <SettingsTab />;
        default:
            return <OverviewTab />;
    }
};

const OverviewTab: React.FC = () => (
    <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <StatCard
                title="Aktive Prosjekter"
                value="24"
                change="+12%"
                positive={true}
                icon="📊"
            />
            <StatCard
                title="Behandlingstid"
                value="45 dager"
                change="-5 dager"
                positive={true}
                icon="⏱️"
            />
            <StatCard
                title="Godkjente Planer"
                value="156"
                change="+8%"
                positive={true}
                icon="✅"
            />
            <StatCard
                title="Ventende Saker"
                value="18"
                change="+3"
                positive={false}
                icon="⏳"
            />
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ChartWidget />
            <RecentActivity />
        </div>
    </div>
);

const StatCard: React.FC<{
    title: string;
    value: string;
    change: string;
    positive: boolean;
    icon: string;
}> = ({ title, value, change, positive, icon }) => (
    <motion.div
        whileHover={{ scale: 1.02 }}
        className="bg-white rounded-xl p-6 shadow-sm border border-gray-100"
    >
        <div className="flex items-center justify-between">
            <div>
                <p className="text-sm font-medium text-gray-600">{title}</p>
                <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
                <p className={`text-sm mt-1 ${positive ? 'text-green-600' : 'text-red-600'}`}>
                    {change} fra forrige måned
                </p>
            </div>
            <div className="text-3xl">{icon}</div>
        </div>
    </motion.div>
);
```

#### Advanced Form Components

```typescript
// frontend/src/components/Forms/AdvancedForm.tsx
import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import DatePicker from 'react-datepicker';
import Select from 'react-select';

const projectSchema = z.object({
    name: z.string().min(1, 'Prosjektnavn er påkrevd'),
    description: z.string().min(10, 'Beskrivelse må være minst 10 tegn'),
    location: z.object({
        address: z.string().min(1, 'Adresse er påkrevd'),
        coordinates: z.tuple([z.number(), z.number()]).optional()
    }),
    type: z.enum(['residential', 'commercial', 'industrial', 'mixed']),
    timeline: z.object({
        startDate: z.date(),
        expectedCompletion: z.date()
    }),
    budget: z.number().positive('Budsjett må være positivt'),
    stakeholders: z.array(z.string()).min(1, 'Minst en interessent må være valgt')
});

type ProjectFormData = z.infer<typeof projectSchema>;

export const ProjectForm: React.FC<{
    onSubmit: (data: ProjectFormData) => void;
    initialData?: Partial<ProjectFormData>;
}> = ({ onSubmit, initialData }) => {
    const {
        register,
        control,
        handleSubmit,
        formState: { errors, isSubmitting },
        watch,
        setValue
    } = useForm<ProjectFormData>({
        resolver: zodResolver(projectSchema),
        defaultValues: initialData
    });

    const projectType = watch('type');

    const stakeholderOptions = [
        { value: 'municipality', label: 'Oslo Kommune' },
        { value: 'developer', label: 'Utbygger' },
        { value: 'residents', label: 'Beboere' },
        { value: 'businesses', label: 'Næringsliv' }
    ];

    return (
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            {/* Basic Information */}
            <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-4">Grunnleggende informasjon</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Prosjektnavn
                        </label>
                        <input
                            {...register('name')}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                            placeholder="Skriv inn prosjektnavn"
                        />
                        {errors.name && (
                            <p className="text-red-500 text-sm mt-1">{errors.name.message}</p>
                        )}
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Prosjekttype
                        </label>
                        <select
                            {...register('type')}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        >
                            <option value="">Velg type</option>
                            <option value="residential">Bolig</option>
                            <option value="commercial">Næring</option>
                            <option value="industrial">Industri</option>
                            <option value="mixed">Blandet</option>
                        </select>
                        {errors.type && (
                            <p className="text-red-500 text-sm mt-1">{errors.type.message}</p>
                        )}
                    </div>
                </div>

                <div className="mt-4">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Beskrivelse
                    </label>
                    <textarea
                        {...register('description')}
                        rows={4}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Beskriv prosjektet..."
                    />
                    {errors.description && (
                        <p className="text-red-500 text-sm mt-1">{errors.description.message}</p>
                    )}
                </div>
            </div>

            {/* Location */}
            <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-4">Lokasjon</h3>
                
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                        Adresse
                    </label>
                    <input
                        {...register('location.address')}
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                        placeholder="Oslo gate 1, 0123 Oslo"
                    />
                    {errors.location?.address && (
                        <p className="text-red-500 text-sm mt-1">{errors.location.address.message}</p>
                    )}
                </div>

                <div className="mt-4">
                    <LocationPicker
                        onLocationSelect={(coords) => setValue('location.coordinates', coords)}
                    />
                </div>
            </div>

            {/* Timeline */}
            <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-4">Tidsplan</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Startdato
                        </label>
                        <Controller
                            name="timeline.startDate"
                            control={control}
                            render={({ field }) => (
                                <DatePicker
                                    selected={field.value}
                                    onChange={field.onChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    dateFormat="dd.MM.yyyy"
                                    placeholderText="Velg startdato"
                                />
                            )}
                        />
                    </div>

                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                            Forventet ferdigstillelse
                        </label>
                        <Controller
                            name="timeline.expectedCompletion"
                            control={control}
                            render={({ field }) => (
                                <DatePicker
                                    selected={field.value}
                                    onChange={field.onChange}
                                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                                    dateFormat="dd.MM.yyyy"
                                    placeholderText="Velg sluttdato"
                                />
                            )}
                        />
                    </div>
                </div>
            </div>

            {/* Stakeholders */}
            <div className="bg-white rounded-lg p-6 shadow-sm">
                <h3 className="text-lg font-semibold mb-4">Interessenter</h3>
                
                <Controller
                    name="stakeholders"
                    control={control}
                    render={({ field }) => (
                        <Select
                            {...field}
                            isMulti
                            options={stakeholderOptions}
                            className="w-full"
                            placeholder="Velg interessenter..."
                            value={stakeholderOptions.filter(option => 
                                field.value?.includes(option.value)
                            )}
                            onChange={(selected) => 
                                field.onChange(selected.map(option => option.value))
                            }
                        />
                    )}
                />
            </div>

            {/* Submit */}
            <div className="flex justify-end space-x-4">
                <button
                    type="button"
                    className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
                >
                    Avbryt
                </button>
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 transition-colors"
                >
                    {isSubmitting ? 'Lagrer...' : 'Lagre prosjekt'}
                </button>
            </div>
        </form>
    );
};
```

### 3.7 Export/Reporting Capabilities

#### Advanced Report Generator

```typescript
// backend/src/services/ReportGenerator.ts
import PDFDocument from 'pdfkit';
import ExcelJS from 'exceljs';
import { createCanvas } from 'canvas';
import Chart from 'chart.js/auto';

export class ReportGenerator {
    async generateProjectReport(projectId: string, format: 'pdf' | 'excel' | 'html'): Promise<Buffer> {
        const project = await this.getProjectData(projectId);
        
        switch (format) {
            case 'pdf':
                return this.generatePDFReport(project);
            case 'excel':
                return this.generateExcelReport(project);
            case 'html':
                return this.generateHTMLReport(project);
            default:
                throw new Error('Unsupported format');
        }
    }

    private async generatePDFReport(project: any): Promise<Buffer> {
        return new Promise((resolve, reject) => {
            const doc = new PDFDocument({ margin: 50 });
            const chunks: Buffer[] = [];

            doc.on('data', chunk => chunks.push(chunk));
            doc.on('end', () => resolve(Buffer.concat(chunks)));
            doc.on('error', reject);

            // Header
            doc.fontSize(20).text('Oslo Planning Report', { align: 'center' });
            doc.moveDown();

            // Project info
            doc.fontSize(16).text('Prosjektinformasjon', { underline: true });
            doc.fontSize(12);
            doc.text(`Navn: ${project.name}`);
            doc.text(`Beskrivelse: ${project.description}`);
            doc.text(`Status: ${project.status}`);
            doc.text(`Opprettet: ${new Date(project.created_at).toLocaleDateString('no-NO')}`);
            doc.moveDown();

            // Timeline chart
            if (project.timeline) {
                doc.addPage();
                doc.fontSize(16).text('Tidsplan', { underline: true });
                
                // Generate chart as image and embed
                this.generateTimelineChart(project.timeline).then(chartBuffer => {
                    doc.image(chartBuffer, 50, doc.y, { width: 500 });
                    doc.moveDown();
                });
            }

            // Documents section
            if (project.documents && project.documents.length > 0) {
                doc.addPage();
                doc.fontSize(16).text('Dokumenter', { underline: true });
                doc.fontSize(12);
                
                project.documents.forEach((doc_item: any, index: number) => {
                    doc.text(`${index + 1}. ${doc_item.original_name}`);
                    doc.text(`   Type: ${doc_item.file_type}`);
                    doc.text(`   Størrelse: ${this.formatFileSize(doc_item.file_size)}`);
                    doc.text(`   Lastet opp: ${new Date(doc_item.created_at).toLocaleDateString('no-NO')}`);
                    doc.moveDown(0.5);
                });
            }

            // Analysis results
            if (project.analysis) {
                doc.addPage();
                doc.fontSize(16).text('Analyse', { underline: true });
                doc.fontSize(12);
                doc.text(`Kategori: ${project.analysis.category}`);
                doc.text(`Konfidensgrad: ${Math.round(project.analysis.confidence * 100)}%`);
                doc.moveDown();
                doc.text('Sammendrag:');
                doc.text(project.analysis.summary, { width: 500 });
            }

            // Footer
            doc.fontSize(10).text(
                `Generert: ${new Date().toLocaleDateString('no-NO')} av Oslo Planning Dashboard`,
                50,
                doc.page.height - 50,
                { align: 'center' }
            );

            doc.end();
        });
    }

    private async generateExcelReport(project: any): Promise<Buffer> {
        const workbook = new ExcelJS.Workbook();
        
        // Project overview sheet
        const overviewSheet = workbook.addWorksheet('Prosjektoversikt');
        
        overviewSheet.addRow(['Prosjektinformasjon']);
        overviewSheet.addRow(['Navn', project.name]);
        overviewSheet.addRow(['Beskrivelse', project.description]);
        overviewSheet.addRow(['Status', project.status]);
        overviewSheet.addRow(['Opprettet', new Date(project.created_at)]);
        
        // Style header
        overviewSheet.getRow(1).font = { bold: true, size: 14 };
        overviewSheet.getColumn(1).width = 20;
        overviewSheet.getColumn(2).width = 50;

        // Documents sheet
        if (project.documents && project.documents.length > 0) {
            const documentsSheet = workbook.addWorksheet('Dokumenter');
            
            documentsSheet.addRow(['Filnavn', 'Type', 'Størrelse', 'Lastet opp']);
            
            project.documents.forEach((doc: any) => {
                documentsSheet.addRow([
                    doc.original_name,
                    doc.file_type,
                    this.formatFileSize(doc.file_size),
                    new Date(doc.created_at)
                ]);
            });
            
            // Style header
            documentsSheet.getRow(1).font = { bold: true };
            documentsSheet.columns.forEach(column => {
                column.width = 20;
            });
        }

        // Analysis sheet
        if (project.analysis) {
            const analysisSheet = workbook.addWorksheet('Analyse');
            
            analysisSheet.addRow(['Analyseresultater']);
            analysisSheet.addRow(['Kategori', project.analysis.category]);
            analysisSheet.addRow(['Konfidensgrad', project.analysis.confidence]);
            analysisSheet.addRow(['Sammendrag', project.analysis.summary]);
            
            if (project.analysis.entities) {
                analysisSheet.addRow([]);
                analysisSheet.addRow(['Identifiserte entiteter']);
                analysisSheet.addRow(['Tekst', 'Type', 'Konfidensgrad']);
                
                project.analysis.entities.forEach((entity: any) => {
                    analysisSheet.addRow([entity.text, entity.label, entity.confidence]);
                });
            }
        }

        return workbook.xlsx.writeBuffer() as Promise<Buffer>;
    }

    private async generateHTMLReport(project: any): Promise<Buffer> {
        const html = `
        <!DOCTYPE html>
        <html lang="no">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Prosjektrapport - ${project.name}</title>
            <style>
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    line-height: 1.6; 
                    margin: 0; 
                    padding: 20px; 
                    background-color: #f5f5f5;
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    background: white; 
                    padding: 30px; 
                    border-radius: 10px; 
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                h1 { 
                    color: #2c3e50; 
                    border-bottom: 3px solid #3498db; 
                    padding-bottom: 10px;
                    text-align: center;
                }
                h2 { 
                    color: #34495e; 
                    margin-top: 30px;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                }
                .info-grid { 
                    display: grid; 
                    grid-template-columns: 1fr 2fr; 
                    gap: 10px; 
                    margin: 20px 0;
                }
                .info-label { 
                    font-weight: bold; 
                    color: #555;
                }
                .document-list { 
                    list-style: none; 
                    padding: 0;
                }
                .document-item { 
                    background: #f8f9fa; 
                    margin: 5px 0; 
                    padding: 10px; 
                    border-left: 3px solid #3498db;
                    border-radius: 5px;
                }
                .analysis-summary { 
                    background: #e8f4fd; 
                    padding: 20px; 
                    border-radius: 8px; 
                    margin: 15px 0;
                }
                .footer { 
                    text-align: center; 
                    margin-top: 40px; 
                    padding-top: 20px; 
                    border-top: 1px solid #ddd; 
                    color: #666;
                    font-size: 12px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Prosjektrapport: ${project.name}</h1>
                
                <h2>Prosjektinformasjon</h2>
                <div class="info-grid">
                    <div class="info-label">Navn:</div>
                    <div>${project.name}</div>
                    <div class="info-label">Beskrivelse:</div>
                    <div>${project.description}</div>
                    <div class="info-label">Status:</div>
                    <div>${project.status}</div>
                    <div class="info-label">Opprettet:</div>
                    <div>${new Date(project.created_at).toLocaleDateString('no-NO')}</div>
                </div>
                
                ${project.documents && project.documents.length > 0 ? `
                <h2>Dokumenter</h2>
                <ul class="document-list">
                    ${project.documents.map((doc: any) => `
                        <li class="document-item">
                            <strong>${doc.original_name}</strong><br>
                            Type: ${doc.file_type} | Størrelse: ${this.formatFileSize(doc.file_size)} | 
                            Lastet opp: ${new Date(doc.created_at).toLocaleDateString('no-NO')}
                        </li>
                    `).join('')}
                </ul>
                ` : ''}
                
                ${project.analysis ? `
                <h2>Analyseresultater</h2>
                <div class="analysis-summary">
                    <p><strong>Kategori:</strong> ${project.analysis.category}</p>
                    <p><strong>Konfidensgrad:</strong> ${Math.round(project.analysis.confidence * 100)}%</p>
                    <p><strong>Sammendrag:</strong></p>
                    <p>${project.analysis.summary}</p>
                </div>
                ` : ''}
                
                <div class="footer">
                    Generert ${new Date().toLocaleDateString('no-NO')} av Oslo Planning Dashboard
                </div>
            </div>
        </body>
        </html>
        `;

        return Buffer.from(html, 'utf-8');
    }

    private async generateTimelineChart(timeline: any): Promise<Buffer> {
        const canvas = createCanvas(800, 400);
        const ctx = canvas.getContext('2d');

        const chart = new Chart(ctx as any, {
            type: 'line',
            data: {
                labels: timeline.milestones?.map((m: any) => m.name) || [],
                datasets: [{
                    label: 'Fremdrift',
                    data: timeline.milestones?.map((m: any) => m.progress) || [],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Prosjektfremdrift'
                    }
                }
            }
        });

        return canvas.toBuffer('image/png');
    }

    private formatFileSize(bytes: number): string {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    private async getProjectData(projectId: string): Promise<any> {
        // This would typically fetch from database
        // For now, return mock data
        return {
            id: projectId,
            name: "Eksempel prosjekt",
            description: "Dette er et eksempelprosjekt for testing av rapportgenerering",
            status: "active",
            created_at: new Date().toISOString(),
            documents: [],
            analysis: null,
            timeline: {
                milestones: [
                    { name: "Start", progress: 100 },
                    { name: "Design", progress: 75 },
                    { name: "Godkjenning", progress: 50 },
                    { name: "Bygging", progress: 25 },
                    { name: "Ferdigstillelse", progress: 0 }
                ]
            }
        };
    }
}
```

## 4. Implementation Timeline

### Phase 1 (Weeks 1-4): Foundation
- Set up project structure
- Implement basic database schema
- Create core React components
- Set up development environment

### Phase 2 (Weeks 5-8): Core Features
- Implement file upload and processing
- Build interactive map component
- Create basic chart visualizations
- Set up offline-first architecture

### Phase 3 (Weeks 9-12): Advanced Features
- Integrate AI/ML capabilities
- Build advanced form components
- Implement export/reporting system
- Add real-time features

### Phase 4 (Weeks 13-16): Polish & Deployment
- Comprehensive testing
- Performance optimization
- UI/UX refinements
- Production deployment setup

## 5. Technology Integration Points

### API Preparation Layers
```typescript
// Abstraction layer for future API integration
interface DataSource {
    fetchProjects(): Promise<Project[]>;
    fetchRegulations(): Promise<Regulation[]>;
    fetchSpatialData(): Promise<GeoJSON>;
}

class MockDataSource implements DataSource {
    // Implementation using local data
}

class OsloAPIDataSource implements DataSource {
    // Future implementation using real APIs
}
```

### Configuration-Driven Data Sources
```typescript
const config = {
    dataSources: {
        projects: process.env.USE_MOCK_DATA ? 'mock' : 'oslo-api',
        regulations: process.env.USE_MOCK_DATA ? 'mock' : 'geonorge',
        spatial: process.env.USE_MOCK_DATA ? 'mock' : 'kartverket'
    }
};
```

This comprehensive development plan provides a roadmap for creating a fully standalone Oslo planning dashboard that can operate independently while being prepared for future API integration. The system will be robust, feature-rich, and capable of handling complex planning data analysis and visualization tasks.