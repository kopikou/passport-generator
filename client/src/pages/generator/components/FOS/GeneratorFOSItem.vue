<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {useQuasar} from "quasar";
import {computed, onBeforeMount, ref, watch} from "vue";
import _ from "lodash";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  fosInfo,
  disabled,
  disciplineThemes,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  title: {
    required: true,
  },
  type: {
    required: true,
  }
})

const $q = useQuasar()
const about = ref('')
const criteria = ref('')

const themes = computed(() => {
  return _.filter(disciplineThemes.value, x => x.formcontrol_verbose == props.title)
})

async function saveData() {
  $q.loading.show({message: "Сохранение данных"})
  _.set(fosInfo.value, `[0].${props.type}`, {
    "about": about.value,
    "criteria": criteria.value,
    "title": props.title,
  })
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": "fos",
    "value": fosInfo.value,
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о фонде оценочных средств дисциплине</span> сохранены!",
      color: "secondary",
      position: "bottom",
      html: true,
    })
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о фонде оценочных средств дисциплине</span> не сохранены!",
      color: "negative",
      position: "bottom",
      html: true,
    })
  })
  $q.loading.hide()
}

watch(additionalInfo, () => {
  about.value = _.get(fosInfo.value, `[0].${props.type}.about`)
  criteria.value = _.get(fosInfo.value, `[0].${props.type}.criteria`)
})

onBeforeMount(() => {
  about.value = _.get(fosInfo.value, `[0].${props.type}.about`)
  criteria.value = _.get(fosInfo.value, `[0].${props.type}.criteria`)
})

</script>

<template>
  <q-expansion-item>

    <template #header>
      <q-item-section>
        {{ props.title }}
        <div>
          <q-chip
            v-for="theme in themes"
            :label="theme.name"
            style="max-width: 60vw"
          >
            <q-tooltip>{{ theme.name }}</q-tooltip>
          </q-chip>
        </div>
      </q-item-section>
    </template>

    <q-card>
      <q-card-section>
        <div class="q-gutter-md">
          <q-input
            label="Описание процедуры"
            type="textarea"
            filled
            stack-label
            v-model="about"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          />
          <q-input
            label="Критерии оценивания"
            type="textarea"
            filled
            stack-label
            v-model="criteria"
            :readonly="disabled"
            debounce="1000"
            @update:modelValue="saveData"
          />
          <!--          <q-btn-->
          <!--            label="Сохранить"-->
          <!--            color="primary"-->
          <!--            @click="saveData"-->
          <!--            v-show="!disabled"-->
          <!--          />-->
        </div>
      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>

</style>
