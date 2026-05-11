import { useEffect, useState } from "react";
import { calculatePlayer, calculateTeam, crawlPlayer, getOptions } from "./api/client.js";

const DEFAULT_POSITIONS = [
  { value: "top", label: "탑" },
  { value: "jungle", label: "정글" },
  { value: "mid", label: "미드" },
  { value: "adc", label: "원딜" },
  { value: "support", label: "서폿" },
];

const LOW_RANK_LABELS = {
  IRON: "아이언",
  BRONZE: "브론즈",
  SILVER: "실버",
  GOLD: "골드",
  PLATINUM: "플래티넘",
  EMERALD: "에메랄드",
  DIAMOND: "다이아",
};

const MASTER_TIERS = new Set(["MASTER", "GRANDMASTER", "CHALLENGER", "MASTER_PLUS"]);

function defaultPeakRank() {
  return { tier: "IRON", division: "4", lp: 0 };
}

function rankToPointTier(rank) {
  if (!rank?.tier) return "실버3 이하";
  if (rank.tier === "IRON" || rank.tier === "BRONZE") return "실버3 이하";
  if (rank.tier === "SILVER") {
    return Number(rank.division) <= 2 ? `실버${rank.division}` : "실버3 이하";
  }
  if (LOW_RANK_LABELS[rank.tier]) return `${LOW_RANK_LABELS[rank.tier]}${rank.division || 4}`;

  const lp = Number(rank.lp || 0);
  if (MASTER_TIERS.has(rank.tier)) {
    if (lp >= 1800) return "마/그/챌 1800 이상";
    const lower = Math.max(Math.floor(lp / 100) * 100, 0);
    return `마/그/챌 ${lower} ~ ${lower + 99}`;
  }

  return "실버3 이하";
}

function makePlayer(position = "top") {
  return {
    gameName: "",
    tagLine: "KR1",
    name: "",
    position,
    participantRank: defaultPeakRank(),
    achievedRank: defaultPeakRank(),
    previousPeakRank: defaultPeakRank(),
    riot: null,
    message: "",
  };
}

function parseRosterText(text) {
  const matches = text.matchAll(/([^#,\s.，、;；/|]+)#([A-Za-z0-9가-힣_-]+)/g);

  return Array.from(matches, (match) => ({
    gameName: match[1].trim(),
    tagLine: match[2].trim(),
    name: match[1].trim(),
  })).slice(0, 5);
}

function toApiPlayer(player) {
  return {
    name: player.name || player.gameName,
    gameName: player.gameName,
    tagLine: player.tagLine,
    position: player.position,
    participantTier: rankToPointTier(player.participantRank),
    achievedTier: rankToPointTier(player.achievedRank),
    previousPeakTier: rankToPointTier(player.previousPeakRank),
  };
}

function RiotLookup({ player, onChange }) {
  return (
    <div className="lookup-row">
      <label>
        닉네임
        <input
          value={player.gameName}
          onChange={(event) => onChange({ gameName: event.target.value, name: event.target.value })}
          placeholder="Hide on bush"
        />
      </label>
      <label>
        태그
        <input
          value={player.tagLine}
          onChange={(event) => onChange({ tagLine: event.target.value })}
          placeholder="KR1"
        />
      </label>
    </div>
  );
}

function RiotSummary({ riot }) {
  if (!riot) return null;

  const solo = riot.soloRank;
  const soloText = solo ? `${solo.tier} ${solo.rank} ${solo.leaguePoints}LP` : "솔로랭크 정보 없음";

  return (
    <div className="riot-summary">
      <strong>
        {riot.account.gameName}#{riot.account.tagLine}
      </strong>
      <span>레벨 {riot.summoner.summonerLevel}</span>
      <span>{soloText}</span>
    </div>
  );
}

function formatScrapedRank(rank) {
  if (!rank?.tier) return "-";
  return `${rank.tier}${rank.lp ? ` ${rank.lp}LP` : ""}`;
}

function AutoSummary({ result }) {
  if (!result) return null;

  return (
    <section className="auto-summary compact-auto-summary" aria-label="자동 추출 결과">
      <div>
        <span>S2025~S2026 최고 티어</span>
        <strong>{formatScrapedRank(result.summary?.best2025To2026)}</strong>
      </div>
      <div>
        <span>S14 최고 티어</span>
        <strong>{formatScrapedRank(result.summary?.best2024)}</strong>
      </div>
      <div>
        <span>전체 기간 최고 티어</span>
        <strong>{formatScrapedRank(result.summary?.allTimeBest)}</strong>
      </div>
    </section>
  );
}

function ErrorBox({ message }) {
  if (!message) return null;

  return (
    <div className="error-box" role="alert">
      <strong>조회에 실패했습니다</strong>
      <p>{message}</p>
      <small>닉네임과 태그를 다시 확인해주세요. 예: Hide on bush#KR1</small>
    </div>
  );
}

function scrapedRankToPointTier(rank) {
  if (!rank?.tier) return "실버3 이하";

  const [tierName, division] = rank.tier.toLowerCase().split(/\s+/);
  const tierMap = {
    iron: "실버3 이하",
    bronze: "실버3 이하",
    silver: division && Number(division) <= 2 ? `실버${division}` : "실버3 이하",
    gold: `골드${division || 4}`,
    platinum: `플래티넘${division || 4}`,
    emerald: `에메랄드${division || 4}`,
    diamond: `다이아${division || 4}`,
  };

  if (["master", "grandmaster", "challenger"].includes(tierName)) {
    return rankToPointTier({ tier: "MASTER_PLUS", lp: Number(rank.lp || 0) });
  }

  return tierMap[tierName] || "실버3 이하";
}

function pointTierToRank(pointTier) {
  if (!pointTier || pointTier === "실버3 이하") return { tier: "SILVER", division: "3", lp: 0 };

  if (pointTier === "마/그/챌 1800 이상") return { tier: "MASTER_PLUS", division: "1", lp: 1800 };

  const masterMatch = pointTier.match(/^마\/그\/챌 (\d+) ~ \d+$/);
  if (masterMatch) return { tier: "MASTER_PLUS", division: "1", lp: Number(masterMatch[1]) };

  const tierMatch = pointTier.match(/^(다이아|에메랄드|플래티넘|골드|실버)([1-4])$/);
  const tierMap = {
    다이아: "DIAMOND",
    에메랄드: "EMERALD",
    플래티넘: "PLATINUM",
    골드: "GOLD",
    실버: "SILVER",
  };

  if (!tierMatch) return defaultPeakRank();
  return { tier: tierMap[tierMatch[1]], division: tierMatch[2], lp: 0 };
}

function ranksFromScrapeSummary(summary) {
  return {
    participantRank: pointTierToRank(scrapedRankToPointTier(summary?.best2025To2026)),
    achievedRank: pointTierToRank(scrapedRankToPointTier(summary?.allTimeBest)),
    previousPeakRank: pointTierToRank(scrapedRankToPointTier(summary?.best2024)),
  };
}

function ScoreCheckPage() {
  const [player, setPlayer] = useState(makePlayer());
  const [result, setResult] = useState(null);
  const [crawlResult, setCrawlResult] = useState(null);
  const [message, setMessage] = useState("");
  const [isCalculating, setIsCalculating] = useState(false);

  function updatePlayer(part) {
    setPlayer((current) => ({ ...current, ...part }));
  }

  async function runAutoCalculation() {
    setMessage("");
    setResult(null);
    setCrawlResult(null);
    setIsCalculating(true);
    try {
      const crawl = await crawlPlayer(player.gameName, player.tagLine);
      const extractedRanks = ranksFromScrapeSummary(crawl.summary);
      const nextPlayer = { ...player, riot: crawl.riot, ...extractedRanks };
      setCrawlResult(crawl);
      setPlayer(nextPlayer);
      setResult(await calculatePlayer(toApiPlayer(nextPlayer)));
    } catch (error) {
      setMessage(error.message);
    } finally {
      setIsCalculating(false);
    }
  }

  async function handleCalculate(event) {
    event.preventDefault();
    await runAutoCalculation();
  }

  return (
    <form className="panel" onSubmit={handleCalculate}>
      <RiotLookup player={player} onChange={updatePlayer} />
      <RiotSummary riot={player.riot} />
      <AutoSummary result={crawlResult} />
      <button className="primary-button" type="submit" disabled={isCalculating}>
        {isCalculating ? "계산 중..." : "포지션별 점수 계산"}
      </button>
      {isCalculating && <p className="form-message loading-message">계산 중입니다. 기록을 불러오고 있어요.</p>}
      <ErrorBox message={message} />

      {result &&
        (() => {
          const lowestPoint = Math.min(...result.positions.map((positionResult) => positionResult.totalPoints));

          return (
            <section className="score-table" aria-label="포지션별 점수">
              {result.positions.map((positionResult) => {
                const gap = positionResult.totalPoints - lowestPoint;

                return (
                  <article key={positionResult.position}>
                    <strong>{positionResult.positionLabel}</strong>
                    <div>기본 {positionResult.basePoints.toFixed(1)}</div>
                    <div>패널티 +{positionResult.dropPenalty.toFixed(1)}</div>
                    <div>최종 {positionResult.totalPoints.toFixed(1)}</div>
                    <small>{gap === 0 ? "가장 낮은 포지션 점수" : `최저 포지션 대비 +${gap.toFixed(1)}점`}</small>
                    <small>적용 티어 {positionResult.effectiveTier}</small>
                    {positionResult.warnings.map((warning) => (
                      <p key={warning}>{warning}</p>
                    ))}
                  </article>
                );
              })}
            </section>
          );
        })()}
    </form>
  );
}

function TeamPage({ positions, pointLimit }) {
  const [players, setPlayers] = useState(() => positions.map((position) => makePlayer(position.value)));
  const [result, setResult] = useState(null);
  const [message, setMessage] = useState("");
  const [rosterText, setRosterText] = useState("");
  const [isCalculating, setIsCalculating] = useState(false);

  useEffect(() => {
    setPlayers((current) =>
      positions.map((position, index) => ({
        ...(current[index] || makePlayer(position.value)),
        position: position.value,
      }))
    );
  }, [positions]);

  function updatePlayer(index, part) {
    setPlayers((current) =>
      current.map((player, playerIndex) =>
        playerIndex === index ? { ...player, ...part } : player
      )
    );
  }

  async function handleCalculate(event) {
    event.preventDefault();
    setMessage("");
    setResult(null);
    setIsCalculating(true);
    try {
      const enrichedPlayers = await Promise.all(
        players.map(async (player) => {
          const crawl = await crawlPlayer(player.gameName, player.tagLine);
          return {
            ...player,
            riot: crawl.riot,
            crawlResult: crawl,
            ...ranksFromScrapeSummary(crawl.summary),
          };
        })
      );
      setPlayers(enrichedPlayers);
      setResult(await calculateTeam(enrichedPlayers.map(toApiPlayer)));
    } catch (error) {
      setResult(null);
      setMessage(error.message);
    } finally {
      setIsCalculating(false);
    }
  }

  function handleApplyRoster() {
    const roster = parseRosterText(rosterText);

    if (roster.length === 0) {
      setMessage("닉네임#태그 형식으로 입력해주세요.");
      return;
    }

    setPlayers((current) =>
      current.map((player, index) => ({
        ...player,
        ...(roster[index] || {}),
      }))
    );
    setResult(null);
    setMessage(`${roster.length}명을 입력란에 채웠습니다.`);
  }

  return (
    <form className="calculator" onSubmit={handleCalculate}>
      <section className="panel compact-panel" aria-label="팀 명단 붙여넣기">
        <label>
          팀 명단 붙여넣기
          <textarea
            value={rosterText}
            onChange={(event) => setRosterText(event.target.value)}
            placeholder="hideonbush#KR1 이지동#0000 청춘청춘청춘#AIM"
          />
        </label>
        <button className="secondary-button" type="button" onClick={handleApplyRoster}>
          입력란 채우기
        </button>
      </section>

      <section className="team-grid" aria-label="팀원 입력">
        {players.map((player, index) => {
          const position = positions.find((item) => item.value === player.position);
          const playerResult = result?.players.find((item) => item.position === player.position);

          return (
            <article className="player-card" key={player.position}>
              <div className="player-card__head">
                <strong>{position?.label}</strong>
                {playerResult && <span>{playerResult.totalPoints.toFixed(1)}점</span>}
              </div>
              <RiotLookup
                player={player}
                onChange={(part) => updatePlayer(index, part)}
              />
              <RiotSummary riot={player.riot} />
              <AutoSummary result={player.crawlResult} />
              {playerResult && (
                <div className="player-result">
                  <div>
                    <span>적용 티어</span>
                    <b>{playerResult.effectiveTier}</b>
                  </div>
                  <div>
                    <span>기본</span>
                    <b>{playerResult.basePoints.toFixed(1)}</b>
                  </div>
                  <div>
                    <span>패널티</span>
                    <b>+{playerResult.dropPenalty.toFixed(1)}</b>
                  </div>
                  <div>
                    <span>최종</span>
                    <b>{playerResult.totalPoints.toFixed(1)}</b>
                  </div>
                </div>
              )}
            </article>
          );
        })}
      </section>

      <section className="summary" aria-label="팀 계산 결과">
        <div>
          <span>팀 총점</span>
          <strong className={result?.isValid === false ? "danger" : ""}>
            {result ? result.totalPoints.toFixed(1) : "0.0"} / {pointLimit}
          </strong>
        </div>
        <div>
          <span>{result?.remainingPoints < 0 ? "초과" : "잔여"}</span>
          <strong>{result ? Math.abs(result.remainingPoints).toFixed(1) : pointLimit.toFixed(1)}점</strong>
        </div>
        <button className="primary-button" type="submit" disabled={isCalculating}>
          {isCalculating ? "계산 중..." : "팀 점수 계산"}
        </button>
        {isCalculating && <p className="form-message loading-message">계산 중입니다. 5명의 기록을 불러오고 있어요.</p>}
        <ErrorBox message={message} />
        {result?.warnings.map((warning) => (
          <p className="form-message danger" key={warning}>
            {warning}
          </p>
        ))}
      </section>
    </form>
  );
}

function App() {
  const [activePage, setActivePage] = useState("score");
  const [options, setOptions] = useState({
    positions: DEFAULT_POSITIONS,
    pointLimit: 165,
  });
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function loadOptions() {
      try {
        const data = await getOptions();
        setOptions({
          positions: data.positions,
          pointLimit: data.pointLimit,
        });
      } catch (error) {
        setMessage(error.message);
      }
    }

    loadOptions();
  }, []);

  return (
    <main className="page">
      <header className="app-header">
        <h1>교류전 점수 계산기</h1>
        <p className="lead">
          닉네임과 태그를 입력하면 기록을 불러와 포지션별 점수와 팀 총점을 계산합니다.
        </p>
      </header>

      <nav className="tabs" aria-label="페이지 선택">
        <button type="button" className={activePage === "score" ? "active" : ""} onClick={() => setActivePage("score")}>
          점수 확인
        </button>
        <button type="button" className={activePage === "team" ? "active" : ""} onClick={() => setActivePage("team")}>
          팀 구성
        </button>
      </nav>

      {message && <p className="form-message danger">{message}</p>}
      {activePage === "score" ? (
        <ScoreCheckPage />
      ) : activePage === "team" ? (
        <TeamPage positions={options.positions} pointLimit={options.pointLimit} />
      ) : (
        <ScoreCheckPage />
      )}
    </main>
  );
}

export default App;
