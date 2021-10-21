type Exposure = string | number;

export class AlbumStats {
    exposures: string[] = [];
    exp_by_iso: {[iso: number]: {[exp: string]: number}} = {};
}
