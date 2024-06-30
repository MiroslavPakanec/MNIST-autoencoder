import { defineStore } from "pinia"
import { Ref, ref } from "vue"

export const useColorStore = defineStore('color', () => {
    const primary: Ref<string> = ref('#57A6A1')
    const secondary: Ref<string> = ref('#240750')
    const ternary: Ref<string> = ref('#cacaca')

    return {
        primary,
        secondary,
        ternary
    }
})