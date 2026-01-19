<template>
  <div class="landing-page">
    <div class="hero-section">
      <div class="hero-content">
        <div class="logo-animation">
          <div class="logo-circle">
            <span class="logo-emoji">{{ currentEmoji }}</span>
          </div>
        </div>

        <h1 class="hero-title">{{ currentMessage.title }}</h1>
        <p class="hero-subtitle">{{ currentMessage.subtitle }}</p>

        <div class="cta-buttons">
          <button @click="goToApp" class="btn-cta btn-primary-cta">
            Get Started
          </button>
          <button @click="scrollToFeatures" class="btn-cta btn-secondary-cta">
            Learn More
          </button>
        </div>

        <div class="message-indicator">
          <span
            v-for="(msg, index) in motivationalMessages"
            :key="index"
            :class="['dot', { active: index === currentMessageIndex }]"
            @click="setMessage(index)"
          ></span>
        </div>
      </div>
    </div>

    <div class="features-section" ref="featuresSection">
      <h2 class="section-title">Why Choose Our Todo App?</h2>

      <div class="features-grid">
        <div v-for="feature in features" :key="feature.title" class="feature-card">
          <div class="feature-icon">{{ feature.icon }}</div>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </div>
    </div>

    <div class="stats-section">
      <div class="stat-item">
        <div class="stat-number">{{ animatedStats.tasks }}+</div>
        <div class="stat-label">Tasks Completed</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{{ animatedStats.users }}+</div>
        <div class="stat-label">Active Users</div>
      </div>
      <div class="stat-item">
        <div class="stat-number">{{ animatedStats.productivity }}%</div>
        <div class="stat-label">Productivity Boost</div>
      </div>
    </div>

    <div class="final-cta">
      <h2>Ready to boost your productivity?</h2>
      <p>Start organizing your tasks today and achieve your goals</p>
      <button @click="goToApp" class="btn-cta btn-primary-cta btn-large">
        Start Now - It's Free
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Landing',
  data() {
    return {
      currentMessageIndex: 0,
      motivationalMessages: [
        {
          title: 'Transform Your Day',
          subtitle: 'Turn your goals into achievements with smart task management',
          emoji: '🚀'
        },
        {
          title: 'Stay Organized',
          subtitle: 'Keep track of what matters most and never miss a deadline',
          emoji: '📋'
        },
        {
          title: 'Achieve More',
          subtitle: 'Boost your productivity and accomplish your dreams',
          emoji: '✨'
        },
        {
          title: 'Work Smarter',
          subtitle: 'Prioritize tasks and focus on what truly drives success',
          emoji: '💡'
        },
        {
          title: 'Stay Focused',
          subtitle: 'Eliminate distractions and concentrate on your priorities',
          emoji: '🎯'
        }
      ],
      features: [
        {
          icon: '⚡',
          title: 'Lightning Fast',
          description: 'Built with modern technologies for instant performance'
        },
        {
          icon: '🎨',
          title: 'Beautiful Design',
          description: 'Clean, intuitive interface that makes task management enjoyable'
        },
        {
          icon: '🔒',
          title: 'Secure & Reliable',
          description: 'Your data is safe with enterprise-grade security'
        },
        {
          icon: '📱',
          title: 'Responsive',
          description: 'Works perfectly on desktop, tablet, and mobile devices'
        },
        {
          icon: '🌙',
          title: 'Dark Mode',
          description: 'Easy on the eyes with automatic theme switching'
        },
        {
          icon: '📊',
          title: 'Analytics',
          description: 'Track your progress with detailed statistics and charts'
        }
      ],
      animatedStats: {
        tasks: 0,
        users: 0,
        productivity: 0
      },
      targetStats: {
        tasks: 10000,
        users: 500,
        productivity: 95
      },
      messageInterval: null,
      statsInterval: null
    }
  },
  computed: {
    currentMessage() {
      return this.motivationalMessages[this.currentMessageIndex]
    },
    currentEmoji() {
      return this.currentMessage.emoji
    }
  },
  mounted() {
    this.startMessageRotation()
    this.animateStats()
  },
  beforeUnmount() {
    if (this.messageInterval) {
      clearInterval(this.messageInterval)
    }
    if (this.statsInterval) {
      clearInterval(this.statsInterval)
    }
  },
  methods: {
    startMessageRotation() {
      this.messageInterval = setInterval(() => {
        this.currentMessageIndex = (this.currentMessageIndex + 1) % this.motivationalMessages.length
      }, 5000)
    },
    setMessage(index) {
      this.currentMessageIndex = index
      // Reset interval
      if (this.messageInterval) {
        clearInterval(this.messageInterval)
      }
      this.startMessageRotation()
    },
    animateStats() {
      const duration = 2000 // 2 seconds
      const steps = 60
      const interval = duration / steps

      let currentStep = 0

      this.statsInterval = setInterval(() => {
        currentStep++
        const progress = currentStep / steps

        this.animatedStats.tasks = Math.floor(this.targetStats.tasks * progress)
        this.animatedStats.users = Math.floor(this.targetStats.users * progress)
        this.animatedStats.productivity = Math.floor(this.targetStats.productivity * progress)

        if (currentStep >= steps) {
          clearInterval(this.statsInterval)
        }
      }, interval)
    },
    goToApp() {
      this.$router.push('/app')
    },
    scrollToFeatures() {
      this.$refs.featuresSection.scrollIntoView({ behavior: 'smooth' })
    }
  }
}
</script>

<style scoped>
.landing-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

/* Hero Section */
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
  pointer-events: none;
}

.hero-content {
  text-align: center;
  max-width: 800px;
  z-index: 1;
}

.logo-animation {
  margin-bottom: 2rem;
}

.logo-circle {
  width: 120px;
  height: 120px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  animation: pulse 2s ease-in-out infinite;
  backdrop-filter: blur(10px);
  border: 3px solid rgba(255, 255, 255, 0.3);
}

.logo-emoji {
  font-size: 4rem;
  animation: rotate 20s linear infinite;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 0 0 rgba(255, 255, 255, 0.7);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 30px 10px rgba(255, 255, 255, 0);
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
  animation: fadeInUp 0.8s ease-out;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 3rem;
  opacity: 0.95;
  animation: fadeInUp 0.8s ease-out 0.2s both;
  font-weight: 300;
  line-height: 1.6;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 0.8s ease-out 0.4s both;
}

.btn-cta {
  padding: 1rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 600;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-primary-cta {
  background: white;
  color: #667eea;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.btn-primary-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 30px rgba(0, 0, 0, 0.3);
}

.btn-secondary-cta {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.btn-secondary-cta:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-3px);
}

.btn-large {
  padding: 1.25rem 3rem;
  font-size: 1.25rem;
}

.message-indicator {
  margin-top: 3rem;
  display: flex;
  gap: 0.75rem;
  justify-content: center;
  animation: fadeInUp 0.8s ease-out 0.6s both;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.4);
  cursor: pointer;
  transition: all 0.3s ease;
}

.dot:hover {
  background: rgba(255, 255, 255, 0.7);
  transform: scale(1.2);
}

.dot.active {
  background: white;
  width: 35px;
  border-radius: 6px;
}

/* Features Section */
.features-section {
  background: white;
  color: #333;
  padding: 6rem 2rem;
}

.section-title {
  text-align: center;
  font-size: 3rem;
  margin-bottom: 4rem;
  color: #667eea;
  font-weight: 700;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: #f8f9fa;
  padding: 2.5rem;
  border-radius: 20px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.feature-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 2s ease-in-out infinite;
}

.feature-card:nth-child(2) .feature-icon {
  animation-delay: 0.2s;
}

.feature-card:nth-child(3) .feature-icon {
  animation-delay: 0.4s;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.feature-card h3 {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: #333;
}

.feature-card p {
  color: #666;
  line-height: 1.6;
}

/* Stats Section */
.stats-section {
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
  padding: 4rem 2rem;
  display: flex;
  justify-content: center;
  gap: 4rem;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}

.stat-label {
  font-size: 1.2rem;
  opacity: 0.9;
  font-weight: 300;
}

/* Final CTA */
.final-cta {
  background: white;
  color: #333;
  padding: 6rem 2rem;
  text-align: center;
}

.final-cta h2 {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #667eea;
  font-weight: 700;
}

.final-cta p {
  font-size: 1.5rem;
  color: #666;
  margin-bottom: 2.5rem;
  font-weight: 300;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .hero-subtitle {
    font-size: 1.2rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-section {
    gap: 2rem;
  }

  .stat-number {
    font-size: 2.5rem;
  }

  .final-cta h2 {
    font-size: 2rem;
  }

  .final-cta p {
    font-size: 1.2rem;
  }
}
</style>
