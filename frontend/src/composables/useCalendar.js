import { MONTHS, WEEK_DAYS, CALENDAR_CONFIG } from '../utils/constants'
import { formatDateForInput } from '../utils/formatters'

export function useCalendar() {
  const showCalendar = { value: false }
  const showYearSelector = { value: false }
  const showMonthSelector = { value: false }
  const tempSelectedDate = { value: null }

  const currentMonth = { value: new Date().getMonth() }
  const currentYear = { value: new Date().getFullYear() }

  const yearRangeStart = {
    value: new Date().getFullYear() - CALENDAR_CONFIG.YEAR_RANGE_START_OFFSET,
  }
  const yearRangeEnd = { value: new Date().getFullYear() + CALENDAR_CONFIG.YEAR_RANGE_END_OFFSET }

  /**
   * Gets current month name
   * @returns {string} - Month name
   */
  const getCurrentMonthName = () => {
    return MONTHS[currentMonth.value]
  }

  // Expose MONTHS and WEEK_DAYS for template use
  const MONTHS_EXPORTED = MONTHS
  const WEEK_DAYS_EXPORTED = WEEK_DAYS

  /**
   * Gets list of available years
   * @returns {number[]} - Array of years
   */
  const getAvailableYears = () => {
    const years = []
    for (let year = yearRangeStart.value; year <= yearRangeEnd.value; year++) {
      years.push(year)
    }
    return years
  }

  /**
   * Generates calendar days for current month
   * @param {string} selectedDate - Currently selected date (YYYY-MM-DD)
   * @returns {Array} - Array of day objects
   */
  const getCalendarDays = selectedDate => {
    const days = []
    const firstDay = new Date(currentYear.value, currentMonth.value, 1)
    const lastDay = new Date(currentYear.value, currentMonth.value + 1, 0)
    const daysInMonth = lastDay.getDate()
    const startingDayOfWeek = (firstDay.getDay() + 6) % 7 // Monday = 0

    const today = new Date()
    const todayStr = formatDateForInput(today)

    // Previous month days
    const prevMonth = new Date(currentYear.value, currentMonth.value, 0)
    const prevMonthDays = prevMonth.getDate()
    for (let i = startingDayOfWeek - 1; i >= 0; i--) {
      const day = prevMonthDays - i
      const dateStr = formatDateForInput(
        new Date(prevMonth.getFullYear(), prevMonth.getMonth(), day)
      )
      days.push({
        day,
        date: dateStr,
        otherMonth: true,
        isToday: false,
        isSelected: false,
        isDisabled: true,
        key: `prev-${day}`,
      })
    }

    // Current month days
    for (let day = 1; day <= daysInMonth; day++) {
      const dateStr = formatDateForInput(new Date(currentYear.value, currentMonth.value, day))
      const isToday = dateStr === todayStr
      const isSelected =
        tempSelectedDate.value === dateStr || (!tempSelectedDate.value && selectedDate === dateStr)

      days.push({
        day,
        date: dateStr,
        otherMonth: false,
        isToday,
        isSelected,
        isDisabled: false,
        key: `curr-${day}`,
      })
    }

    // Next month days (to fill the grid)
    const remainingDays = CALENDAR_CONFIG.CALENDAR_GRID_SIZE - days.length
    for (let day = 1; day <= remainingDays; day++) {
      const dateStr = formatDateForInput(new Date(currentYear.value, currentMonth.value + 1, day))
      days.push({
        day,
        date: dateStr,
        otherMonth: true,
        isToday: false,
        isSelected: false,
        isDisabled: true,
        key: `next-${day}`,
      })
    }

    return days
  }

  /**
   * Navigates to previous month
   */
  const previousMonth = () => {
    if (currentMonth.value === 0) {
      currentMonth.value = 11
      currentYear.value--
    } else {
      currentMonth.value--
    }
    showYearSelector.value = false
    showMonthSelector.value = false
  }

  /**
   * Navigates to next month
   */
  const nextMonth = () => {
    if (currentMonth.value === 11) {
      currentMonth.value = 0
      currentYear.value++
    } else {
      currentMonth.value++
    }
    showYearSelector.value = false
    showMonthSelector.value = false
  }

  /**
   * Selects a year
   * @param {number} year - Year to select
   */
  const selectYear = year => {
    currentYear.value = year
    showYearSelector.value = false

    // Adjust range if needed
    if (year < yearRangeStart.value) {
      const diff = yearRangeStart.value - year
      yearRangeStart.value = year
      yearRangeEnd.value -= diff
    } else if (year > yearRangeEnd.value) {
      const diff = year - yearRangeEnd.value
      yearRangeEnd.value = year
      yearRangeStart.value += diff
    }
  }

  /**
   * Selects a month
   * @param {number} monthIndex - Month index (0-11)
   */
  const selectMonth = monthIndex => {
    currentMonth.value = monthIndex
    showMonthSelector.value = false
  }

  /**
   * Navigates year range backward
   */
  const previousYearRange = () => {
    const range = yearRangeEnd.value - yearRangeStart.value + 1
    yearRangeStart.value -= range
    yearRangeEnd.value -= range
  }

  /**
   * Navigates year range forward
   */
  const nextYearRange = () => {
    const range = yearRangeEnd.value - yearRangeStart.value + 1
    yearRangeStart.value += range
    yearRangeEnd.value += range
  }

  /**
   * Selects a date
   * @param {Object} day - Day object
   */
  const selectDate = day => {
    if (day.isDisabled || day.otherMonth) return
    tempSelectedDate.value = day.date
  }

  /**
   * Resets calendar to current date
   */
  const resetToCurrentDate = () => {
    const now = new Date()
    currentMonth.value = now.getMonth()
    currentYear.value = now.getFullYear()
    tempSelectedDate.value = null
  }

  return {
    showCalendar,
    showYearSelector,
    showMonthSelector,
    tempSelectedDate,
    currentMonth,
    currentYear,
    yearRangeStart,
    yearRangeEnd,
    MONTHS: MONTHS_EXPORTED,
    WEEK_DAYS: WEEK_DAYS_EXPORTED,
    getCurrentMonthName,
    getAvailableYears,
    getCalendarDays,
    previousMonth,
    nextMonth,
    selectYear,
    selectMonth,
    previousYearRange,
    nextYearRange,
    selectDate,
    resetToCurrentDate,
  }
}
