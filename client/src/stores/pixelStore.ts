import { defineStore } from "pinia"
import { Ref, ref } from "vue"

export type Mask = { sx: number, ex: number, sy: number, ey: number }

export const usePixelStore = defineStore('pixels', () => {
    const dim: Ref<number> = ref(28)
    const pixels: Ref<number[][]> = ref([])
    const isProcessing: Ref<boolean> = ref(false)
    const masks: Ref<Mask[]> = ref([])
    const maxMasks: Ref<number> = ref(5)

    const reset = (): void => {
        const matrix: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
              row.push(255)
            }
            matrix.push(row)
        }
        pixels.value = matrix
        masks.value = []
    }

    const invert = (pixels: number[][]): number[][] => {
        const inverted: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                row.push(255 - pixels[i][j])
            }
            inverted.push(row)
        }
        return inverted
    }

    const scale = (pixels: number[][]): number[][] => {
        const scaled: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                const value: number = Math.round(clamp(pixels[i][j], 0, 255))
                row.push(value)
            }
            scaled.push(row)
        }
        return scaled
    }

    const rotate = (pixels: number[][]): number[][] => {
        const rotated: number[][] = []
        for (let i = 0; i < dim.value; i++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                row.push(pixels[j][i])
            }
            rotated.push(row)
        }
        return rotated
    }

    const rotateCounterClockwise = (pixels: number[][]): number[][] => {
        const dim = pixels.length;
        const rotated: number[][] = [];
        for (let i = 0; i < dim; i++) {
            const row: number[] = [];
            for (let j = 0; j < dim; j++) {
                row.push(pixels[i][j]);
            }
            rotated.push(row);
        }
        return rotated;
    }

    const mask = (pixels: number[][], m: Mask): number[][] => {
        const masked: number[][] = []
        for (let i = 0; i < dim.value; i ++) {
            const row: number[] = []
            for (let j = 0; j < dim.value; j++) {
                if (i >= m.sx && i <= m.ex && j >= m.sy && j <= m.ey) row.push(0)
                else row.push(pixels[j][i])
            }
            masked.push(row)
        }
        return masked
    }

    const reshape = (pixels: number[]): number[][] => {
        if (pixels.length !== dim.value * dim.value) throw 'Attempting to process digit with invalid dimentions'
        const processedDigit: number[][] = []
        let rowIndex = 0;
        let row: number[] = []
        for (const pixel of pixels) {
            if (rowIndex >= dim.value) {
                processedDigit.push(row)
                rowIndex = 0
                row = []
            }
            row.push(pixel)
            rowIndex += 1
        }
        processedDigit.push(row)
        return processedDigit
    }

    const flatten = (pixels: number[][]): number[] => {
        const flat: number[] = []
        for (let i = 0; i < dim.value; i++) {
            for (let j = 0; j < dim.value; j++) {
                flat.push(pixels[j][i]);
            }
        }
        return flat
    }

    const setPixels = (rawPixels: number[]): void => {
        isProcessing.value = true
        const reshaped: number[][] = reshape(rawPixels)
        const scaled: number[][] = scale(reshaped)
        const inverted: number[][] = invert(scaled)
        const rotated: number[][] = rotate(inverted)
        isProcessing.value = false
        pixels.value = rotated
    }

    const setPixelsWithMask = (rawPixels: number[], mask_shape: Mask): void => {
        if (masks.value.length >= maxMasks.value) return
        isProcessing.value = true
        const reshaped: number[][] = reshape(rawPixels)
        const scaled: number[][] = scale(reshaped)
        const inverted: number[][] = invert(scaled)
        const masked: number[][] = mask(inverted, mask_shape)
        isProcessing.value = false
        pixels.value = masked
        masks.value.push(mask_shape)
    }

    const getPixels = (): number[][] => pixels.value
    
    const getFlatPixels = (): number[] => {
        const inverted: number[][] = invert(pixels.value)
        const rotated: number[][] = rotateCounterClockwise(inverted)
        const flattened: number[] = flatten(rotated)
        return flattened
    }

    const clamp = (value: number, min: number, max: number): number => Math.min(Math.max(value, min), max)
    
    return { getPixels, getFlatPixels, setPixelsWithMask, setPixels, masks, maxMasks, isProcessing, reset, mask, reshape }
})