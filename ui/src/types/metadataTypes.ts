type Executable = {
    name: string;
    type: string;
    location: string;
};

type Metadata = {
    description: string;
    version: string;
    tag: string;
    authorName: string;
    digest: string;
    specifications: string[];
};

type Resources = {
    cores: {
        min: number;
        max: number;
    };
    memory: {
        min: number;
        max: number;
    };
};

export type SoftwareMetadata = {
    executable: Executable;
    metadata: Metadata;
    resources: Resources;
};

export type SoftwareDetails = {
    softwareName: string | null,
    softwareType: string | null,
}