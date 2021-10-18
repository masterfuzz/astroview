export class AlbumDetail {
    path!: string;
    glob!: string;
    unique_name!: string;
    images!: string[];
    notes!: string[];
    sequences!: string[];
    image_notes!: object;

    constructor() {
        this.path = "UNKNOWN";
        this.glob = "*.RAW";
        this.unique_name = "VU5LTk9XTgo=";
        this.images = [];
        this.notes = [];
        this.sequences = [];
        this.image_notes = {};
    }
}
