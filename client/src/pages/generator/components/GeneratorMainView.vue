<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, onBeforeMount, ref, watch, watchEffect} from "vue";
import _ from "lodash";
import {api} from "boot/axios";
import {useQuasar} from "quasar";

const generatorViewStore = useGeneratorViewStore()
const $q = useQuasar()
const {
  cafData,
  rpdData,
  semestersData,
  activeRpdId,
  additionalInfo,
  disciplineGoal,
  disabled,
  admissionData,
  planlinesData,
} = storeToRefs(generatorViewStore)

const displGoal = ref()
const saveData = _.debounce(async () => {
  // console.log(displGoal)
  saveDiscplineGoal()
}, 1000)

const toolbar = ref([
  ['bold', 'italic', 'strike', 'underline', 'subscript', 'superscript'],
  [
    {
      label: 'Стиль текста',
      icon: 'mdi-format-color-text',
      fixedLabel: true,
      options: ['h4', 'h5', 'h6', 'p', 'code'],
    },
  ],
  [
    {
      label: 'Размер текста',
      icon: 'mdi-format-size',
      fixedLabel: true,
      list: 'no-icons',
      options: ['size-1', 'size-2', 'size-3', 'size-4', 'size-5'],
    },
    'removeFormat'
  ],
  ['quote', 'unordered', 'ordered', 'outdent', 'indent'],
  ['undo', 'redo'],
  ['fullscreen'],
])

async function saveDiscplineGoal() {
  $q.loading.show()
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    type: "disciplineGoal",
    value: displGoal.value,
  }).then((v) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о цели освоения дисциплины</span> сохранены!",
      color: "secondary",
      position: "bottom-right",
      html: true,
    })
    let key = _.findKey(additionalInfo.value, (x) => x.id == v.data.id)
    _.set(additionalInfo.value, `[${key}].value`, displGoal.value)
  }, (rej) => {
    $q.notify({
      message: "Данные <span class='text-bold'>о цели освоения дисциплины</span> не сохранены!",
      color: "negative",
      position: "bottom-right",
      html: true,
    })
  })
  $q.loading.hide()
}

const practiceName = computed(() => {
  let result = rpdData.value.planlines?.dis.split(/:\s*/)
  return {
    'type': result[0] ?? '',
    'text': _.capitalize(result[1] ?? ''),
  }
})

function getPracticeNamePart(text) {

}

function getSpecNapr(name) {
  const names = name.split("направленность")
  if (names.length > 1) {
    return names[1].replace(' - ', '')
  } else {
    return 'Отсутствует'
  }
}

function getSpecName(name) {
  const names = name.split("направленность")
  if (names.length > 1) {
    return names[0].replace(', ', '')
  } else {
    return name
  }
}

const can_be_copied_by_anyone = computed({
  get() {
    return rpdData.value.can_be_copied_by_anyone
  },
  async set(value) {
    await api.post(`api/generator/${activeRpdId.value}/toggle-can-be-copied-by-anyone/`)
    rpdData.value.can_be_copied_by_anyone = !rpdData.value.can_be_copied_by_anyone;
  }
});

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

watch(additionalInfo, () => {
  displGoal.value = disciplineGoal.value
}, {immediate: true})

</script>

<template>

  <div class="q-px-md">
    <span class="text-h6" v-if="planlinesData.viewpract">Данные по практике</span>
    <span class="text-h6" v-else>Данные по дисциплине</span>
    <div class="flex">
      Данные для рабочей программы
      <span v-if="planlinesData.viewpract">практики</span>
      <span v-else>по дисциплине</span>
      "{{ rpdData.planlines?.dis }}" получены автоматически из учебного плана
    </div>
    <div>
      <a target="__blank" :href="rpdData.plx_file">Скачать *.plx</a>
    </div>
    <q-separator class="q-mt-md q-mb-md"/>
    <div>
      <q-toggle v-model="can_be_copied_by_anyone">Разрешить копировать дисциплину любому преподавателю (т.е. любой преподаватель сможет скопировать себе в РПД данные, которые вы внесли, при условии совпадения названия дисциплины)</q-toggle>
    </div>
    <q-separator class="q-mt-md q-mb-md"/>
    <div v-if="rpdData.users">
      <div v-if="rpdData.users.developer"><b>Разработал:</b> {{rpdData.users.developer}}</div>
      <div v-if="rpdData.users.confirmed"><b>Согласовал:</b> {{rpdData.users.confirmed}}</div>
      <div v-if="rpdData.users.accepted"><b>Утвердил:</b> {{rpdData.users.accepted}}</div>
    </div>
    <q-separator class="q-mt-md q-mb-md"/>
    <div class="q-pb-md">
      <div v-if="!planlinesData.viewpract">
        <span class="text-subtitle1">Наименование дисциплины</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ rpdData.planlines?.dis }}</div>
          </template>
        </q-field>
      </div>
      <div v-else>
        <span class="text-subtitle1">Вид практики</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ practiceName.type }}</div>
          </template>
        </q-field>
        <span class="text-subtitle1">Тип практики</span>
        <q-field outlined dense>
          <template v-slot:control>
            <div class="self-center full-width no-outline">{{ practiceName.text }}</div>
          </template>
        </q-field>
      </div>
      <span v-if="admissionData?.cadmkind != 5" class="text-subtitle1">Профиль/Специальность</span>
      <q-field outlined dense v-if="admissionData?.cadmkind != 5">
        <template v-slot:control>
          <div class="self-center full-width no-outline">{{ rpdData.admission?.spec_name }}</div>
        </template>
      </q-field>
      <span v-if="admissionData?.cadmkind != 5" class="text-subtitle1">Наименование направления</span>
      <q-field outlined dense v-if="admissionData?.cadmkind != 5">
        <template v-slot:control>
          <div class="self-center full-width no-outline">{{ rpdData.admission?.direct_name }}</div>
        </template>
      </q-field>
      <span v-if="admissionData?.cadmkind == 5" class="text-subtitle1">Наименование направления</span>
      <q-field outlined dense v-if="admissionData?.cadmkind == 5">
        <template v-slot:control>
          <div class="self-center full-width no-outline">{{ getSpecName(rpdData.admission?.spec_name) }}</div>
        </template>
      </q-field>
      <span v-if="admissionData?.cadmkind == 5" class="text-subtitle1">Направленность</span>
      <q-field outlined dense v-if="admissionData?.cadmkind == 5">
        <template v-slot:control>
          <div class="self-center full-width no-outline">{{ getSpecNapr(rpdData.admission?.spec_name) }}</div>
        </template>
      </q-field>
      <span class="text-subtitle1">Факультет</span>
      <q-field outlined dense>
        <template v-slot:control>
          <div class="self-center full-width no-outline">{{ admissionData?.cfac__name }}</div>
        </template>
      </q-field>
      <span class="text-subtitle1">Кафедра</span>
      <q-field outlined dense>
        <template v-slot:control>
          <div class="self-center full-width no-outline">{{ cafDataById[rpdData.planlines?.caf]?.label }}</div>
        </template>
      </q-field>
    </div>

    <div class="flex justify-center items-center">
      <span class="text-subtitle1">Количество семестров</span>
      <q-field filled dense style="width: 5%" class="q-ml-md q-mr-md">
        <template v-slot:control>
          <div class="self-center full-width no-outline text-center">{{ semestersData.length }}</div>
        </template>
      </q-field>
      <span class="text-subtitle1">Начальный семестр</span>
      <q-field filled dense style="width: 5%" class="q-ml-md">
        <template v-slot:control>
          <div class="self-center full-width no-outline text-center">{{ semestersData[0]?.num }}</div>
        </template>
      </q-field>
    </div>
    <q-separator class="q-mt-md q-mb-md"/>
    <div>
      <!--        <q-input-->
      <!--          label="Цель освоения дисциплины"-->
      <!--          type="textarea"-->
      <!--          filled-->
      <!--          stack-label-->
      <!--          v-model="displGoal"-->
      <!--          class="q-mb-md"-->
      <!--          :readonly="disabled"-->
      <!--          hint="Для аннотации"-->
      <!--          debounce="1000"-->
      <!--          @update:modelValue="saveDiscplineGoal"-->
      <!--        />-->
      <!--        <q-editor-->
      <!--          v-model="displGoal"-->
      <!--          :toolbar="toolbar"-->
      <!--          @update:modelValue="saveData"-->
      <!--        />-->

    </div>
  </div>
</template>

<style scoped lang="scss">

</style>
